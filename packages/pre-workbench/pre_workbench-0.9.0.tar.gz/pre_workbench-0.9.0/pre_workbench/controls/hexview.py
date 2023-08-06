#!/usr/bin/python3
# -*- coding: utf-8 -*-
# PRE Workbench
# Copyright (C) 2022 Mira Weller
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import json
import logging
import re
import sys
from base64 import b64decode
from collections import namedtuple
from typing import List, Union, Tuple

from math import ceil, floor

from PyQt5.QtCore import (Qt, QSize, pyqtSignal)
from PyQt5.QtGui import QPainter, QFont, QColor, QPixmap, QFontMetrics, QKeyEvent, QStatusTipEvent, QMouseEvent, QPen
from PyQt5.QtWidgets import QApplication, QMenu, QSizePolicy, QAction, QInputDialog, QMessageBox, \
	QAbstractScrollArea

from pre_workbench.bbuf_parsing import apply_grammar_on_bbuf
from pre_workbench import configs, guihelper
from pre_workbench.algo.range import Range
from pre_workbench.configs import SettingsSection
from pre_workbench.guihelper import setClipboardText, showWidgetDlg, getClipboardText, APP, filledColorIcon
from pre_workbench.app import GlobalEvents
from pre_workbench.controls.hexview_selheur import SelectionHelpers
from pre_workbench.objects import ByteBuffer, parseHexFromClipboard, BidiByteBuffer, ByteBufferList
from pre_workbench.rangetree import RangeTreeWidget
from pre_workbench.structinfo.format_info import builtinTypes
from pre_workbench.structinfo.parser import parse_definition
from pre_workbench.util import PerfTimer

group = SettingsSection('HexView2', 'Hex Editor', 'address', 'Address Styles')
configs.registerOption(group, 'Color', 'Address Color', 'color', {}, '#888888',None)
configs.registerOption(group, 'Format', 'Address Format', 'text', {}, '{:08x}',None)

group = SettingsSection('HexView2', 'Hex Editor', 'hex', 'Hex Styles')
configs.registerOption(group, 'Font', 'Font', 'font', {}, 'monospace,12,-1,7,50,0,0,0,0,0',None)
configs.registerOption(group, 'Color', 'Hex Color', 'color', {}, '#ffffff', None)
configs.registerOption(group, 'SpaceAfter', 'Hex SpaceAfter', 'int', {'min': 1, 'max': 1024}, 8, None)
configs.registerOption(group, 'SpaceWidth', 'Hex SpaceWidth', 'int', {'min': 1, 'max': 1024}, 8, None)
configs.registerOption(group, 'Format', 'Hex Format', 'select', {'options':[
	('{:02x}', "Hexadecimal"),
	('{:08b}', "Binary"),
	('{:04o}', "Octal"),
	('{:03d}', "Decimal"),
]}, '{:02x}', None)

group = SettingsSection('HexView2', 'Hex Editor', 'ascii', 'ASCII Styles')
configs.registerOption(group, 'Color', 'ASCII Color', 'color', {}, '#bbffbb', None)

group = SettingsSection('HexView2', 'Hex Editor', 'section', 'Section Styles')
configs.registerOption(group, 'Font', 'Font', 'font', {}, 'Arial,10,-1,0,50,0,0,0,0,0',None)
configs.registerOption(group, 'Color', 'Section Color', 'color', {}, '#aaaaaa', None)

group = SettingsSection('HexView2', 'Hex Editor', 'general', 'General')
configs.registerOption(group, 'lineHeight', 'lineHeight', 'double', {'min': 0.1, 'max': 10}, 1.3, None)
configs.registerOption(group, 'bytesPerLine', 'bytesPerLine', 'int', {'min': 1, 'max': 1024}, 16, None)
configs.registerOption(group, 'backgroundColor', 'backgroundColor', 'color', {}, '#333333', None)

pattern_heading = re.compile("[#]{0,6}")

HitTestResult = namedtuple('HitTestResult', ['buffer', 'offset', 'region'])
SelectionHeuristicMatch = namedtuple('SelectionHeuristicMatch', ['buffer', 'start', 'end', 'description', 'color'])

class HexView2(QAbstractScrollArea):
	onNewSubflowCategory = pyqtSignal(str, object)
	parseResultsUpdated = pyqtSignal(list)
	selectionChanged = pyqtSignal(object)

	buffers: List[ByteBuffer]

	def __init__(self, byteBuffer=None, annotationSetDefaultName="", options=dict(), optionsConfigKey="HexViewParams", project=None, formatInfoContainer=None):
		super().__init__()
		self.project = project
		self.formatInfoContainer = formatInfoContainer
		if self.formatInfoContainer: self.formatInfoContainer.updated.connect(self._formatInfoUpdated)
		logging.debug("HexView - formatInfoContainer = %r", self.formatInfoContainer)
		self.annotationSetDefaultName = annotationSetDefaultName
		self.buffers = list()
		#self.firstLine = 0
		#self.scrollY = 0
		#self.partialLineScrollY = 0
		self.setFocusPolicy(Qt.StrongFocus)

		self.backgroundPixmap = QPixmap()
		self.textPixmap = QPixmap()
		GlobalEvents.on_config_change.connect(self._loadOptions)
		self._loadOptions()

		self.pixmapsInvalid = True
		self.selBuffer = 0
		self.selStart = 0
		self.selEnd = 0
		self.clickGrammarUndefRef = None
		self.clickGrammarFieldRef = None
		self.selHeurMatches = list()
		self.itemY = list()
		self.lastHit = None
		self.selecting = False
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self._onCustomContextMenuRequested)
		if byteBuffer is None:
			self.setBytes(bytes())
		else:
			self.setBuffer(byteBuffer)
		self.setMouseTracking(True)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

	@property
	def scrollY(self):
		return self.verticalScrollBar().value()

	@scrollY.setter
	def scrollY(self, value):
		self.verticalScrollBar().setValue(value)

	@property
	def firstLine(self):
		return floor(self.scrollY / self.dyLine)

	@property
	def partialLineScrollY(self):
		return self.scrollY - (self.dyLine * self.firstLine)

	def _loadOptions(self, *dummy):
		self.bytesPerLine = configs.getValue('HexView2.general.bytesPerLine')
		self.addressFormat = configs.getValue('HexView2.address.Format')
		self.hexFormat = configs.getValue('HexView2.hex.Format')
		bgcolor = configs.getValue('HexView2.general.backgroundColor')
		if bgcolor == 'auto':
			import darkdetect
			if darkdetect.isDark():
				bgcolor = '#333333'
			else:
				bgcolor = '#ffffff'
		self.backgroundColor = QColor(bgcolor)

		self.fontAddress = self.fontHex = self.fontAscii = QFont()
		self.fontHex.fromString(configs.getValue('HexView2.hex.Font'))

		self.xAddress = 5
		#self.fontAddress = QFont()
		#self.fontAddress.fromString(configs.getValue('HexView2.address.Font'))
		self.fsAddress = QColor(configs.getValue('HexView2.address.Color'))

		self.xHex = QFontMetrics(self.fontAddress).width(self.addressFormat.format(0)) + 15
		#self.fontHex = QFont()
		#self.fontHex.fromString(configs.getValue('HexView2.hex.Font'))
		self.fsHex = QColor(configs.getValue('HexView2.hex.Color'));	self.dxHex = QFontMetrics(self.fontHex).width(self.hexFormat.format(0))+4
		self.hexSpaceAfter = configs.getValue('HexView2.hex.SpaceAfter'); self.hexSpaceWidth = configs.getValue('HexView2.hex.SpaceWidth')

		self.xAscii = self.xHex + self.dxHex*self.bytesPerLine+(ceil(self.bytesPerLine/self.hexSpaceAfter)-1)*self.hexSpaceWidth+15
		#self.fontAscii = QFont()
		#self.fontAscii.fromString(configs.getValue('HexView2.ascii.Font'))
		self.fsAscii = QColor(configs.getValue('HexView2.ascii.Color')); self.dxAscii = QFontMetrics(self.fontAscii).width("W")

		self.fsSel = QColor("#7fddaaff");  self.fsCursor = QColor("#bfddaaff");  self.fsHover = QColor("#8fff9bff")
		sectionFont = QFont(); sectionFont.fromString(configs.getValue('HexView2.section.Font'))
		self.fontSection = []
		for i in [0,10,8,6,4,2]:
			f = QFont(sectionFont)
			f.setPointSize(f.pointSize() + i)
			self.fontSection.append(f)
		self.fsSection = QColor(configs.getValue('HexView2.section.Color'));

		self.charHeight = QFontMetrics(self.fontHex).height()
		self.dyLine = ceil(self.charHeight * configs.getValue('HexView2.general.lineHeight'))
		self.fontAscent = ceil(QFontMetrics(self.fontHex).ascent())
		self.linePadding = ceil(max(0, self.charHeight * (configs.getValue('HexView2.general.lineHeight') - 1) / 2))

		#self.fiTreeWidget.move(self.xAscii + self.dxAscii*self.bytesPerLine + 10, 10)
		self.redraw()


	############ HEX VIEW CONTEXT MENU  #############################################################

	def _onCustomContextMenuRequested(self, point):
		hit = self._hitTest(point)
		ctxMenu = QMenu("Context menu", self)
		if hit is not None:
			if hit.offset < self.selFirst() or hit.offset > self.selLast() or hit.buffer != self.selBuffer:
				self.select(hit.offset, hit.offset, hit.buffer, False)
			self._buildSelectionContextMenu(ctxMenu)
		else:
			self._buildGeneralContextMenu(ctxMenu)
		ctxMenu.exec(self.mapToGlobal(point))

	def _buildSelectionContextMenu(self, ctx):
		ctx.addAction(QAction("Copy Selection as Hex\tCtrl-C", ctx, triggered=lambda: self.copySelection(), shortcut="Ctrl+C"))
		ctx.addAction("Copy Selection C Array", lambda: self.copySelection((", ", "0x%02X")))
		ctx.addAction("Copy Selection Hexdump\tCtrl-Shift-C", lambda: self.copySelection("hexdump"))
		#ctx.addAction("Copy selected annotations", lambda: self.copySelection("hexdump"))
		if len(self.selHeurMatches) > 0:
			mnu = ctx.addMenu("Selection Heuristic Matches")
			for match in self.selHeurMatches:
				mnu.addAction(filledColorIcon(match.color, 16), "[%d:%d] %s" % (match.start, match.end-1, match.description),
							  lambda match=match: self.select(match.start, match.end-1, match.buffer))
		ctx.addSeparator()
		#ctx.addAction("Selection %d-%d (%d bytes)"%(self.selStart,self.selEnd,self.selLength()))
		#ctx.addAction("Selection 0x%X - 0x%X (0x%X bytes)"%(self.selStart,self.selEnd,self.selLength()))
		if self.clickGrammarUndefRef:
			for name, (length, fun) in builtinTypes.items():
				if length == self.selLength() and fun:
					ctx.addAction(name, lambda name=name: self.clickGrammarAdd(name))
			ctx.addAction(f"BYTES[{self.selLength()}]", lambda: self.clickGrammarAdd(f"BYTES[{self.selLength()}]"))
			ctx.addAction(f"STRING[{self.selLength()}]", lambda: self.clickGrammarAdd(f"STRING[{self.selLength()}](charset=\"utf8\")"))
			ctx.addAction("struct { ... }", lambda: self.clickGrammarAdd("struct { _undef_1 BYTES[" + str(self.selLength()) + "] }"))
			ctx.addAction("bits { ... }", lambda: self.clickGrammarAdd("bits { _undef_1 : " + str(self.selLength()*8) + " }"))
			ctx.addSeparator()
		if self.clickGrammarFieldRef:
			ctx.addAction("Undefine field " + self.clickGrammarFieldRef[0].field_name, self.clickGrammarUndefine)
			ctx.addSeparator()

		try:
			match = next(
				self.buffers[self.selBuffer].matchRanges(start=self.selFirst(), end=self.selLast()+1, doesntHaveMetaKey='_sdef_ref'))

			ctx.addAction("&Delete Selected Style\tX", lambda: self.deleteSelectedStyle())

			ctx.addSeparator()
		except StopIteration:
			pass
		for key, name, style in guihelper.getHighlightStyles():
			ctx.addAction(name+"\t"+key, lambda style=style: self.styleSelection(**style))
		ctx.addSeparator()
		ctx.addAction("&Start Section...", lambda: self.setSectionSelection())
		ctx.addSeparator()

		if self.selLength() > 1:
			if self.project:
				menu = ctx.addMenu( "Apply Annotation Set For Selection")
				for name in self.project.getAnnotationSetNames():
					#TODO implement this
					menu.addAction(name, lambda name=name: print(name))
			self._buildParseBufferSubmenu(ctx, "Parse Selection", -1, None)
		else:
			self._buildLoadAnnotationSetSubmenu(ctx, "Load Annotation Set", self.selBuffer, self.buffers[self.selBuffer].annotation_set_name)
			self._buildParseBufferSubmenu(ctx, "Parse Buffer", self.selBuffer, self.buffers[self.selBuffer].fi_root_name)
			self._buildRunMacroOnBufferSubmenu(ctx, "Run Macro On Buffer", self.selBuffer)

		menu = ctx.addMenu("Run Macro On Selection")
		for container_id, container, macroName in APP().find_macros_by_input_types(["BYTE_ARRAY"]):
			menu.addAction(macroName, lambda c=container, name=macroName: c.getMacro(name).execute(self.getRangeBytes(self.selRange())))

	def _buildGeneralContextMenu(self, ctx):
		ctx.addAction("Select all", lambda: self.selectAll())
		ctx.addSeparator()
		ctx.addAction("Paste", lambda: self.setBuffer(parseHexFromClipboard()))
		menu = ctx.addMenu("Paste as")
		menu.addAction("Base64", lambda: self.setBuffer(ByteBuffer(b64decode(getClipboardText()))))
		ctx.addAction("Clear Annotations" + (" on All Buffers" if len(self.buffers) > 1 else ""), lambda: self.clearRanges())

		self._buildLoadAnnotationSetSubmenu(ctx, "Load Annotation Set" + (" on All Buffers" if len(self.buffers) > 1 else ""), None,
											valueifsame(buf.annotation_set_name for buf in self.buffers))

		self._buildParseBufferSubmenu(ctx, "Parse" + (" All Buffers" if len(self.buffers) > 1 else " Buffer"), None,
											valueifsame(buf.fi_root_name for buf in self.buffers))
		self._buildRunMacroOnBufferSubmenu(ctx, "Run Macro On" + (" All Buffers" if len(self.buffers) > 1 else " Buffer"), None)

	def _buildLoadAnnotationSetSubmenu(self, ctx, title, bufIdx, current):
		if self.project:
			menu = ctx.addMenu(title)
			for name in self.project.getAnnotationSetNames():
				act = menu.addAction(name, lambda name=name: self.loadAnnotations(name, bufIdx))
				act.setCheckable(True)
				act.setChecked(name == current)
			menu.addAction("New...", lambda: self.loadAnnotations(QInputDialog.getText(self, "Annotation Set", "Please enter a name for the new annotation set:")[0], bufIdx))

	def _buildParseBufferSubmenu(self, ctx, title, bufIdx, current):
		if self.formatInfoContainer:
			menu = ctx.addMenu(title)
			for name in self.formatInfoContainer.definitions.keys():
				act = menu.addAction(name, lambda name=name: self.applyFormatInfo(name, bufIdx))
				act.setCheckable(True)
				act.setChecked(name == current)
			if bufIdx is not None and bufIdx >= 0:
				menu.addAction("New...", lambda: self._newGrammarDef(
					QInputDialog.getText(self, "New Grammar Definition", "Please enter a name for the new grammar definition:")[0],bufIdx))

	def _newGrammarDef(self, name, bufIdx):
		if not name: return
		bbuf = self.buffers[bufIdx]
		self.formatInfoContainer.definitions[name] = parse_definition('struct(endianness=">") { _undef_1 BYTES[' + str(bbuf.length) + '] }')
		self.formatInfoContainer.write_file(self.formatInfoContainer.file_name)
		self.applyFormatInfo(name, bufIdx)

	def _buildRunMacroOnBufferSubmenu(self, ctx, title, bufIdx):
		menu = ctx.addMenu(title)
		for container_id, container, macroName in APP().find_macros_by_input_types(["BYTE_BUFFER", "BYTE_BUFFER_LIST"]):
			menu.addAction(macroName, lambda c=container, name=macroName: self._runMacroOnBuffer(c, name, bufIdx))

	def _runMacroOnBuffer(self, container, macroname, bufIdx):
		macro = container.getMacro(macroname)
		bufs = self.buffers if bufIdx is None else [self.buffers[bufIdx]]
		if macro.input_type == "BYTE_BUFFER":
			for buf in bufs:
				macro.execute(buf)
		elif macro.input_type == "BYTE_BUFFER_LIST":
			lst = ByteBufferList()
			for buf in bufs:
				lst.add(buf)
			macro.execute(lst)

	def clickGrammarAdd(self, definitionStr):
		new_field_name = QInputDialog.getText(self, "New Field", "Please enter a name for the new field of type "+definitionStr+":")[0]
		if not new_field_name: return
		bytes_range, struct_range = self.clickGrammarUndefRef
		bytes = bytes_range.metadata['_sdef_ref']
		struct = struct_range.metadata['_sdef_ref']
		if any(True for i, el in enumerate(struct.fi.children) if el[0] == new_field_name):
			QMessageBox.warning(self, "Error", "The struct already contains a field named \"" + new_field_name + "\"")
			return

		sel = self.selRange()
		idx = next(i for i, el in enumerate(struct.fi.children) if el[0] == bytes_range.field_name)

		# resize or remove current _undef_
		offset_in_bytes = sel.start - bytes_range.start
		if offset_in_bytes > 0:
			from pre_workbench.structinfo.expr import deserialize_expr
			bytes.updateParams(size=deserialize_expr(str(offset_in_bytes)))
			idx += 1
		else:
			del struct.fi.children[idx]

		# insert new field
		new_def = parse_definition(definitionStr)
		new_def_size = sel.length()
		struct.fi.children.insert(idx, (new_field_name, new_def, ''))
		idx += 1

		# insert new _undef_ behind new field, if needed
		remaining_size = bytes_range.length() - offset_in_bytes - new_def_size
		if remaining_size > 0:
			new_bytes_def = parse_definition(f'BYTES[{remaining_size}]')
			struct.fi.children.insert(idx, ('_undef_XXX', new_bytes_def, ''))

		# re-number all _undef_ fields
		self._clickGrammarRenumber(struct_range)

		self.formatInfoContainer.write_file(self.formatInfoContainer.file_name)

	def clickGrammarUndefine(self):
		field_range, struct_range = self.clickGrammarFieldRef
		struct = struct_range.metadata['_sdef_ref']

		start = end = next(i for i, el in enumerate(struct.fi.children) if el[0] == field_range.field_name)
		undef_len = field_range.length()
		if start > 0 and struct.fi.children[start - 1][0].startswith('_undef_'):
			undef_len += struct.fi.children[start - 1][1].fi.size_expr.evaluate_dict({})
			start -= 1
		if end + 1 < len(struct.fi.children) and struct.fi.children[end + 1][0].startswith('_undef_'):
			undef_len += struct.fi.children[end + 1][1].fi.size_expr.evaluate_dict({})
			end += 1

		logging.debug(f"clickGrammarUndefine: replacing {start} to {end} with BYTES[{undef_len}]")
		struct.fi.children[start:end+1] = [('_undef_', parse_definition(f'BYTES[{undef_len}]'), '')]

		# re-number all _undef_ fields
		self._clickGrammarRenumber(struct_range)

		self.formatInfoContainer.write_file(self.formatInfoContainer.file_name)



	def _clickGrammarRenumber(self, struct_range):
		struct = struct_range.metadata['_sdef_ref']
		number = 1
		for i in range(len(struct.fi.children)):
			name, fi, comment = struct.fi.children[i]
			if name.startswith('_undef_'):
				struct.fi.children[i] = (f'_undef_{number}', fi, comment)
				number += 1
		

	def setDefaultAnnotationSet(self, name):
		self.annotationSetDefaultName = name
		self.loadAnnotations(name)

	def loadAnnotations(self, set_name, bufIdx=None):
		if not set_name: return
		for buf in self.buffers if bufIdx is None else [self.buffers[bufIdx]]:
			buf.setRanges(buf.matchRanges(hasMetaKey='_sdef_ref'))
			if set_name is not None:
				annotations = self.project.getAnnotations(set_name)
				for rowid, start, end, meta_str in annotations:
					meta = json.loads(meta_str)
					if meta.get("deleted"): continue
					meta['rowid'] = rowid
					buf.addRange(Range(start=start, end=end, meta=meta))
			buf.annotation_set_name = set_name
		self.redraw()

	def storeAnnotation(self, range):
		if not self.project: return
		buf = self.buffers[self.selBuffer]
		if not buf.annotation_set_name:
			buf.annotation_set_name, ok = QInputDialog.getText(self, "Annotation Set", "Please enter a name for the new annotation set:")
			if not ok or not buf.annotation_set_name: return
		self.project.storeAnnotation(buf.annotation_set_name, range)

	def clearRanges(self):
		for buf in self.buffers:
			buf.clearRanges()
			buf.annotation_set_name = None
		self.redraw()

	def getRangeBytes(self, range):
		return self.buffers[range.buffer_idx].getBytes(range.start, range.length())

	def getRangeString(self, range, style=(" ","%02X")):
		if isinstance(style, tuple):
			return self.buffers[range.buffer_idx].toHex(range.start, range.length(), style[0], style[1])
		elif style=="hexdump":
			return self.buffers[range.buffer_idx].toHexDump(range.start, range.length())

	def copySelection(self, style=(" ","%02X")):
		setClipboardText(self.getRangeString(self.selRange(), style))

	def styleSelection(self, **kw):
		selection = self.selRange()
		try:
			match = next(self.buffers[self.selBuffer].matchRanges(start=self.selFirst(), end=self.selLast()+1, doesntHaveMetaKey='_sdef_ref'))
		except StopIteration:
			match = selection
			self.buffers[self.selBuffer].addRange(selection)

		match.metadata.update(kw)
		self.storeAnnotation(match)
		self.redraw()

	def setSectionSelection(self):
		selection = self.selRange()
		try:
			match = next(self.buffers[self.selBuffer].matchRanges(start=selection.start, doesntHaveMetaKey='_sdef_ref'))
			title = match.metadata.get("section")
		except StopIteration:
			match = None
			title = ""

		newTitle, ok = QInputDialog.getText(self, "Section", "Enter section title:", text=title)
		if ok:
			if match is None:
				match = selection
				self.buffers[self.selBuffer].addRange(selection)
			match.metadata.update(section=newTitle)
			self.storeAnnotation(match)
			self.redraw()

	def deleteSelectedStyle(self):
		try:
			match = next(
				self.buffers[self.selBuffer].matchRanges(start=self.selFirst(), end=self.selLast()+1, doesntHaveMetaKey='_sdef_ref'))
			self.buffers[self.selBuffer].removeRange(match)
			match.metadata["deleted"] = True
			self.storeAnnotation(match)
			self.redraw()
		except StopIteration:
			pass


	################# FI Tree ####################################################

	def _formatInfoUpdated(self):
		self.applyFormatInfo()

	def applyFormatInfo(self, root_name=None, bufIdx=None):
		for buf in self.buffers if bufIdx is None else [self.buffers[bufIdx]]:
			if root_name is not None: buf.fi_root_name = root_name
			apply_grammar_on_bbuf(buf, buf.fi_root_name, self._newSubflowCategory)
		self.parseResultsUpdated.emit([buf.fi_tree for buf in self.buffers])
		self.redraw()

	def _newSubflowCategory(self, category, parse_context, **kv):
		logging.debug("on_new_subflow_category: %r",category)
		self.onNewSubflowCategory.emit(category, parse_context)
		logging.debug("on_new_subflow_category done: %r",category)

	def _fiTreeItemSelected(self, item, previous):
		if item is None: return
		range = item.data(0, RangeTreeWidget.RangeRole)
		if range is not None:
			self.selectRange(range, scrollIntoView=True)
		#source = item.data(0, RangeTreeWidget.SourceDescRole)
		#if isinstance(source, structinfo.AbstractFI):
			#self.on_data_selected.emit(source)



	#############  SCROLLING  ###########################################

	def wheelEvent(self, e):
		if e.pixelDelta().isNull():
			deltaY = e.angleDelta().y() / 4
		else:
			deltaY = e.pixelDelta().y()
		if deltaY == 0: return
		self.scrollY = max(0, min((self.maxLine()-1)*self.dyLine, self.scrollY - deltaY))
		logging.debug("wheelEvent deltaY=%d scrollY=%d partial=%d",deltaY,self.scrollY,self.partialLineScrollY)
		#self.redraw()

	def scrollIntoView(self, bufIndex:int, offset:int):
		line = self.byteOffsetToLineNumber(bufIndex, offset)
		if line < self.firstLine:
			self._setFirstLine(line - 2)
		elif line >= self.maxVisibleLine():
			self._setFirstLine(line - 5)  #TODO - ich weiß vorher nicht, wie viele zeilen auf den schirm passen

	def _setFirstLine(self, line):
		self.scrollY = max(0, min(self.maxLine()-1, line)) * self.dyLine
		#self.redraw()

	############## MOUSE EVENTS - SELECTION  ############################

	def mouseMoveEvent(self, e):
		hit = self._hitTest(e.pos())
		if hit == self.lastHit: return
		self.lastHit = hit
		if self.selecting and hit is not None and hit.buffer == self.selBuffer: self.selEnd = hit.offset
		self.redrawSelection()

	def mousePressEvent(self, e):
		if e.button() != Qt.LeftButton: return
		hit = self._hitTest(e.pos())
		if hit is None: return
		self.lastHit = hit
		self.selStart = self.selEnd = hit.offset
		self.selBuffer = hit.buffer
		self.selecting = True
		self.redrawSelection()
		
	def mouseReleaseEvent(self, e):
		if e.button() != Qt.LeftButton: return
		self.selecting = False
		self.select(self.selStart, self.selEnd)

	def mouseDoubleClickEvent(self, e: QMouseEvent) -> None:
		if e.button() != Qt.LeftButton: return

		try:
			match = next(self.buffers[0].matchRanges(contains=self.selFirst(), doesntHaveMetaKey='_sdef_ref'))
			self.select(match.start, match.end-1)
		except StopIteration:
			pass

		hit = self._hitTest(e.pos())
		if hit and hit.region == 'ascii':
			start, end = self._extendRangeMatch(hit.offset, hit.buffer, lambda c: 32 < c < 128)
			self.select(start, end, hit.buffer)

	def _extendRangeMatch(self, start, bufIdx, matcher):
		end = start
		buf = self.buffers[bufIdx]
		if not matcher(buf.buffer[start]): return (start, start)
		while start > 0:
			if not matcher(buf.buffer[start - 1]): break
			start -= 1
		while end < buf.length - 1:
			if not matcher(buf.buffer[end + 1]): break
			end += 1
		return (start,end)

	def _hitTest(self, point):
		dx = -self.horizontalScrollBar().value()
		x, y = point.x()-dx, point.y()
		linePos = None
		if (x >= self.xAscii):
			pos = floor((x - self.xAscii) / self.dxAscii)
			if (pos < self.bytesPerLine): linePos = pos; region = 'ascii'
		elif (x >= self.xHex):
			xx = (x - self.xHex)
			xx -= floor(xx / (self.dxHex*self.hexSpaceAfter + self.hexSpaceWidth)) * self.hexSpaceWidth # correction factor for hex grouping
			pos = floor(xx / self.dxHex)
			if (pos < self.bytesPerLine): linePos = pos; region = 'hex'

		if (linePos is None): return None

		for i in range(linePos, len(self.itemY), self.bytesPerLine):
			bufIdx, bufOffset, itemY = self.itemY[i]
			if itemY is not None and itemY <= y and y <= itemY+self.dyLine:
				return HitTestResult(bufIdx, bufOffset, region)

		return None


	def selFirst(self):
		return min(self.selStart, self.selEnd)
	def selLast(self):
		return max(self.selStart, self.selEnd)
	def selLength(self):
		return max(self.selStart, self.selEnd) - self.selFirst() + 1
	def selRange(self):
		return Range(min(self.selStart,self.selEnd), max(self.selStart,self.selEnd)+1, buffer_idx=self.selBuffer)

	def _clipPosition(self, bufferIdx, pos):
		if bufferIdx >= len(self.buffers): return 0
		return max(0, min(len(self.buffers[bufferIdx]) - 1, pos))

	def select(self, start:int, end:int, bufferIdx=None, scrollIntoView=False):
		if bufferIdx is None: bufferIdx = self.selBuffer
		#TODO ensure that start, end are in valid range
		self.selStart = self._clipPosition(bufferIdx, start); self.selEnd = self._clipPosition(bufferIdx, end)
		self.selBuffer = bufferIdx
		if scrollIntoView:
			self.scrollIntoView(bufferIdx, self.selEnd)
			self.scrollIntoView(bufferIdx, self.selStart)

		self.redrawSelection()
		logging.log(logging.TRACE, "selection changed %r-%r (%r)",self.selStart, self.selEnd, self.lastHit)
		r = self.selRange()

		#self.fiTreeWidget.hilightFormatInfoTree(r)

		with PerfTimer("selectionChanged event handlers"):
			shortest = None
			self.clickGrammarUndefRef = None
			self.clickGrammarFieldRef = None
			if self.selBuffer < len(self.buffers):
				self.selectionChanged.emit(r)

				def is_fi_type(range, typeName):
					return hasattr(range.metadata.get('_sdef_ref'), 'fi_type') and range.metadata['_sdef_ref'].fi_type == typeName

				ranges = list(self.buffers[self.selBuffer].matchRanges(containsRange=self.selRange(), hasMetaKey='_sdef_ref'))
				if len(ranges) >= 2 and is_fi_type(ranges[1], 'StructFI'):
					if (is_fi_type(ranges[0], 'FieldFI') and ranges[0].metadata['_sdef_ref'].fi.format_type == 'BYTES'
							and ranges[0].field_name.startswith('_undef_')):
						self.clickGrammarUndefRef = (ranges[0], ranges[1])
						logging.debug("clickGrammar Match! / bytes: %r / struct: %r",ranges[0],ranges[1])
					else:
						self.clickGrammarFieldRef = (ranges[0], ranges[1])
				try:
					shortest = min(ranges, key=len)
				except ValueError:
					pass

			QApplication.postEvent(self, QStatusTipEvent("Buffer #%d  Selection %d-%d (%d bytes)   0x%X - 0x%X (0x%X bytes)    %r   %s"%(
				self.selBuffer, self.selStart,self.selEnd,self.selLength(),self.selStart,self.selEnd,self.selLength(),shortest,"ClickGrammar Available!" if self.clickGrammarUndefRef else "")))


	def selectRange(self, rangeObj, scrollIntoView=False):
		self.select(rangeObj.start, max(rangeObj.start, rangeObj.end-1), bufferIdx=rangeObj.buffer_idx, scrollIntoView=scrollIntoView)

	def selectAll(self):
		self.select(0, len(self.buffers[self.selBuffer]), self.selBuffer)



	######## KEYBOARD EVENTS ###########################################

	def keyPressEvent(self, e: QKeyEvent) -> None:
		mod = e.modifiers() & ~Qt.KeypadModifier

		arrow = None
		if e.key() == Qt.Key_Left:
			arrow = self.selEnd - 1
		elif e.key() == Qt.Key_Right:
			arrow = self.selEnd + 1
		elif e.key() == Qt.Key_Up:
			arrow = self.selEnd - self.bytesPerLine
		elif e.key() == Qt.Key_Down:
			arrow = self.selEnd + self.bytesPerLine
		elif e.key() == Qt.Key_PageUp:
			arrow = self.selEnd - self.bytesPerLine * floor(self.height() / self.dyLine * 0.9)
		elif e.key() == Qt.Key_PageDown:
			arrow = self.selEnd + self.bytesPerLine * floor(self.height() / self.dyLine * 0.9)

		if arrow is not None:
			arrow = self._clipPosition(self.selBuffer, arrow)
			self.scrollIntoView(self.selBuffer, arrow)

		if arrow is not None and mod == Qt.ShiftModifier:
			self.select(self.selStart, arrow)

		elif arrow is not None and mod == Qt.NoModifier:
			self.select(arrow, arrow)

		elif mod == Qt.ControlModifier:
			if e.key() == Qt.Key_A:
				self.selectAll()
			elif e.key() == Qt.Key_C:
				self.copySelection()
			elif e.key() == Qt.Key_F5:
				self.applyFormatInfo()
			elif e.key() == Qt.Key_Plus:
				self.zoomIn()
			elif e.key() == Qt.Key_Minus:
				self.zoomOut()
			elif e.key() == Qt.Key_0:
				self.zoomReset()

		elif mod == Qt.ControlModifier | Qt.ShiftModifier:
			if e.key() == Qt.Key_C:
				self.copySelection("hexdump")

		elif mod == Qt.NoModifier:
			if e.key() == Qt.Key_X:
				self.deleteSelectedStyle()

			if Qt.Key_A <= e.key() <= Qt.Key_Z:
				letter = chr(e.key() - Qt.Key_A + 0x41)
				styles = guihelper.getHighlightStyles()
				info = next((x for x in styles if x[0] == letter), None)
				if info:
					self.styleSelection(**info[2])

		else:
			super().keyPressEvent(e)

	def focusInEvent(self, event) -> None:
		self.viewport().update()

	def focusOutEvent(self, event) -> None:
		self.viewport().update()

	def zoomIn(self):
		self.fontHex.setPointSize(self.fontHex.pointSize() + 1)
		configs.setValue('HexView2.hex.Font', self.fontHex.toString())
		GlobalEvents.on_config_change.emit()

	def zoomOut(self):
		self.fontHex.setPointSize(self.fontHex.pointSize() - 1)
		configs.setValue('HexView2.hex.Font', self.fontHex.toString())
		GlobalEvents.on_config_change.emit()

	def zoomReset(self):
		self.fontHex.setPointSize(10)
		configs.setValue('HexView2.hex.Font', self.fontHex.toString())
		GlobalEvents.on_config_change.emit()

	#################  data setters   ##########################################
	def getBytes(self):
		return self.buffers[0].buffer  # TODO handle multiple buffers!

	def setBytes(self, buf : bytes):
		abuf = ByteBuffer(buf)
		self.setBuffer(abuf)
	
	def setBuffer(self, bbuf : Union[ByteBuffer, BidiByteBuffer, List[ByteBuffer]]):
		if isinstance(bbuf, BidiByteBuffer):
			self.buffers = bbuf.buffers
		elif isinstance(bbuf, ByteBuffer):
			self.buffers = [ bbuf ]
		elif isinstance(bbuf, list) and all(isinstance(item, ByteBuffer) for item in bbuf):
			self.buffers = bbuf
		else:
			raise TypeError("Invalid type passed to HexView2.setBuffer: "+str(type(bbuf)))
		self.scrollY = 0
		self.verticalScrollBar().setMaximum(self.maxLine() * self.dyLine)
		self.parseResultsUpdated.emit([buf.fi_tree for buf in self.buffers])
		self.select(0, 0, 0)
		self.redraw()

	############ RENDERING ############################################################

	def resizeEvent(self, e):
		self.redraw()
		self.verticalScrollBar().setPageStep(self.height())
		self.horizontalScrollBar().setPageStep(self.width())
		self.horizontalScrollBar().setMaximum(max(0, self.xAscii + self.dxAscii * (self.bytesPerLine+3) - self.width()))
		#self.fiTreeWidget.resize(self.width() - self.fiTreeWidget.pos().x()-10, self.height()-40)

	def sizeHint(self):
		return QSize(self.xAscii + self.dxAscii * self.bytesPerLine + 10, 256)

	def scrollContentsBy(self, dx, dy):
		self.redraw()

	def redraw(self):
		self.pixmapsInvalid = True
		for buffer in self.buffers:
			buffer.invalidateCaches()
		self.viewport().update()

	def drawPixmaps(self):
		if self.size().height() < 3 or self.size().width() < 3: return
		with PerfTimer("drawPixmaps"):
			if self.size() != self.backgroundPixmap.size():
				self.backgroundPixmap = QPixmap(self.size())
				self.textPixmap = QPixmap(self.size())
			self.backgroundPixmap.fill(self.backgroundColor)
			self.textPixmap.fill(QColor("#00000000"))

			qpBg = QPainter()
			qpBg.begin(self.backgroundPixmap)
			qpTxt = QPainter()
			qpTxt.begin(self.textPixmap)
			self._drawLines(qpTxt, qpBg)
			qpBg.end()
			qpTxt.end()

	def redrawSelection(self):
		self.viewport().update()

	def paintEvent(self, e):
		with PerfTimer("paintEvent"):
			if self.pixmapsInvalid:
				try:
					self.drawPixmaps()
				except:
					logging.exception("Failed to draw bg/text pixmaps")
				self.pixmapsInvalid = False
			try:
				qp = QPainter()
				qp.begin(self.viewport())
				qp.drawPixmap(0, 0, self.backgroundPixmap)
				self._drawSelection(qp)
				self._drawHover(qp)
				qp.drawPixmap(0, 0, self.textPixmap)
				#self.drawQuicktip(qp)
				qp.end()
			except:
				logging.exception("Failed to render HexView")

	def _drawLines(self, qpTxt, qpBg):
		y = 0 - self.partialLineScrollY
		canvasHeight = self.size().height()
		self.itemY = list()
		if len(self.buffers) == 0: return
		maxLine = self.maxLine()
		lineNumber = self.firstLine
		while y < canvasHeight and lineNumber < maxLine:
			while len(self.itemY) % self.bytesPerLine != 0:
				self.itemY.append((None, None, None))

			y = self._drawLine(qpTxt, qpBg, lineNumber, y)
			lineNumber += 1
	
	def _drawLine(self, qpTxt, qpBg, lineNumber, y):
		TXT_DY = self.fontAscent + self.linePadding
		dx = -self.horizontalScrollBar().value()

		bufIdx, offset, _ = self.lineNumberToByteOffset(lineNumber)
		buffer = self.buffers[bufIdx]
		if offset == 0:
			# draw buffer separator
			qpBg.fillRect(dx+2,int(y),100,1,QColor("red"))
			qpTxt.setFont(self.fontSection[0]); qpTxt.setPen(self.fsAscii)
			qpTxt.drawText(dx+self.xHex, int(y+self.fontSection[0].pointSize() * 1.7), repr(buffer.metadata))
			y += self.fontSection[0].pointSize() * 2

		end = min(len(buffer), offset + self.bytesPerLine)
		ii = 0
		for i in range(offset, end):
			# if specified, print section header
			#sectionAnnotations = buffer.getAnnotationValues(start=i, annotationProperty="section");
			sectionAnnotations = buffer.ranges.getMetaValuesStartingAt(i, "section")
			if len(sectionAnnotations) != 0:
				if (ii != 0): y += self.dyLine;
				qpTxt.setPen(self.fsSection)
				for row in sectionAnnotations:
					bangs = len(pattern_heading.match(row).group())
					qpTxt.setFont(self.fontSection[bangs])
					qpTxt.drawText(dx+self.xHex, int(y+self.fontSection[bangs].pointSize() * 1.7), row)
					y += self.fontSection[bangs].pointSize() * 2
				qpTxt.setFont(self.fontAddress)
				qpTxt.setPen(QColor("#555555"))
				if (ii != 0): qpTxt.drawText(dx+self.xAddress, int(y+TXT_DY), self.addressFormat.format(i));

			if (ii == 0):  #print address for first byte in line
				qpTxt.setFont(self.fontAddress)
				qpTxt.setPen(self.fsAddress)
				qpTxt.drawText(dx+self.xAddress, int(y+TXT_DY), self.addressFormat.format(offset))

			# if specified, draw background color from style attribute
			bg = buffer.getStyle(i, "color", None)
			fg = buffer.getStyle(i, "textcolor", None)
			if (bg):
				qpBg.fillRect(dx+self.xHex + ii * self.dxHex + int(ii/self.hexSpaceAfter)*self.hexSpaceWidth + 2, int(y+1), self.dxHex, self.dyLine-2, QColor(bg))
				qpBg.fillRect(dx+self.xAscii + ii * self.dxAscii, int(y+1), self.dxAscii, self.dyLine-2, QColor(bg))

			# store item's Y position and buffer pos
			self.itemY.append((bufIdx, i, int(y)))

			# print HEX and ASCII representation of this byte
			theByte = buffer.getByte(i)
			qpTxt.setFont(self.fontHex)
			qpTxt.setPen( self.fsHex if not fg else QColor(fg))
			qpTxt.drawText(dx+self.xHex + ii * self.dxHex + int(ii/self.hexSpaceAfter)*self.hexSpaceWidth + 2, int(y+TXT_DY), self.hexFormat.format(theByte))
			qpTxt.setFont(self.fontAscii)
			qpTxt.setPen(self.fsAscii if not fg else QColor(fg))
			asciichar = chr(theByte) if (theByte > 0x20 and theByte < 0x80) else "."
			qpTxt.drawText(dx+self.xAscii + ii * self.dxAscii, int(y+TXT_DY), asciichar)
			ii += 1

		return y + self.dyLine

	def _drawSelection(self, qp):
		self.selHeurMatches.clear()
		if len(self.buffers) == 0 or len(self.itemY) == 0: return

		selMin = min(self.selStart, self.selEnd)
		selMax = max(self.selStart, self.selEnd)
		selVisibleMin = max(self.itemY[0][1], selMin) if self.itemY[0][0] == self.selBuffer else selMin
		selVisibleMax = min(self.itemY[-1][1], selMax) if self.itemY[-1][0] == self.selBuffer else selMax
		for i in range(selVisibleMin, selVisibleMax+1):
			(xHex, xAscii, y, dy) = self.offsetToClientPos(self.selBuffer, i)
			if dy is None: break
			fs = self.fsCursor if i == self.selEnd and self.hasFocus() else self.fsSel
			qp.fillRect(xHex, y, self.dxHex, dy, fs)
			qp.fillRect(xAscii, y, self.dxAscii, dy, fs)

		for helper, meta in SelectionHelpers.types:
			if configs.getValue("SelHeur." + helper.__name__ + ".enabled", meta.get("defaultEnabled", False)):
				with PerfTimer("execution of selectionHelper (%s)", helper.__name__):
					helper(self, qp, self.buffers[self.selBuffer], (self.selBuffer, selMin, selMax), configs.getValue("SelHeur."+helper.__name__+".options", {}))

	def _drawHover(self, qp):
		if self.lastHit is not None:
			(xHex, xAscii, y, dy) = self.offsetToClientPos(self.lastHit.buffer, self.lastHit.offset)
			if dy is not None:
				qp.fillRect(xHex, y, self.dxHex, dy, self.fsHover)
				qp.fillRect(xAscii, y, self.dxAscii, dy, self.fsHover)

			if len(self.selHeurMatches) > 0:
				startY = self.height()-10
				for match in self.selHeurMatches:
					if match.buffer == self.lastHit.buffer and match.start <= self.lastHit.offset and match.end > self.lastHit.offset:
						qp.setPen(QColor(match.color))
						qp.drawText(10, startY, "[%d:%d] %s" % (match.start, match.end-1, match.description))
						startY -= 15

	def highlightMatch(self, qp: QPainter, matchrange: Tuple[int, int, int], desc: str, color: QColor):
		(bufIdx, start, end) = matchrange
		self.selHeurMatches.append(SelectionHeuristicMatch(bufIdx, start, end, desc, color))
		((firstBuf, firstOffset), (lastBuf, lastOffset)) = self.visibleRange()
		if bufIdx == firstBuf and start < firstOffset: start = firstOffset
		for i in range(start, end):
			(xHex, xAscii, y, dy) = self.offsetToClientPos(bufIdx, i)
			if dy is None: break
			p = QPen(color)
			p.setWidth(3)
			qp.setPen(p)
			qp.drawLine(xHex + 3, y + dy, xHex + self.dxHex - 3, y + dy)
			qp.drawLine(xAscii + 1, y + dy, xAscii + self.dxAscii - 2, y + dy)

	########### CALCULATION    #########################
	def lineNumberToByteOffset(self, lineNumber:int) -> HitTestResult:
		bufOffset = lineNumber * self.bytesPerLine
		bufIdx = 0
		while bufIdx < len(self.buffers) and bufOffset >= len(self.buffers[bufIdx]):
			bufOffset -= ceil(len(self.buffers[bufIdx]) / self.bytesPerLine) * self.bytesPerLine
			bufIdx += 1
		return HitTestResult(bufIdx, bufOffset, None)

	def byteOffsetToLineNumber(self, bufIndex:int, offset:int) -> int:
		linesBefore = sum(ceil(len(buffer) / self.bytesPerLine) for buffer in self.buffers[:bufIndex-1]) if bufIndex > 0 else 0
		return linesBefore + floor(offset / self.bytesPerLine)

	def maxLine(self):
		return sum(ceil(len(buffer) / self.bytesPerLine) for buffer in self.buffers);

	def maxVisibleLine(self):
		return self.firstLine + ceil(len(self.itemY)/self.bytesPerLine)

	def offsetToClientPos(self, buffer:int, offset:int):
		dx = -self.horizontalScrollBar().value()
		column = offset % self.bytesPerLine
		for bufIdx, bufOffset, itemY in self.itemY:
			if bufIdx == buffer and bufOffset == offset:
				return (dx+self.xHex + column * self.dxHex + int(column / self.hexSpaceAfter) * self.hexSpaceWidth,
						dx+self.xAscii + self.dxAscii * column,
						itemY + floor(self.linePadding * 0.5),
						ceil(self.charHeight * 1.2))
		logging.warning("trying to paint outside viewport %r", offset)
		return (None, None, None, None)

	def visibleRange(self):
		firstBuf, firstOffset, firstY = self.itemY[0]
		lastBuf, lastOffset, lastY = self.itemY[-1]
		return ((firstBuf, firstOffset), (lastBuf, lastOffset))


def valueifsame(iterable):
	s = set(iterable)
	return next(iter(s)) if len(s) == 1 else None


def showHexView2Dialog(parent, title, content, ok_callback):
	hexview = HexView2()
	hexview.setBytes(content)
	return showWidgetDlg(hexview, title, lambda: hexview.getBytes(), ok_callback)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = HexView2()
	ex.show()
	ex.setBytes(open(sys.argv[1], "rb").read())
	sys.exit(app.exec_())

