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


import logging
import os
import sys
import traceback
import uuid
from glob import glob

from PyQt5.QtCore import (Qt, pyqtSlot, QSignalMapper, QTimer, pyqtSignal, QUrl)
from PyQt5.QtGui import QKeySequence, QColor, QDesktopServices
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QWidget, QMessageBox, QToolButton, QLabel, QApplication, \
	QPushButton, QTextBrowser, QDialogButtonBox
from PyQtAds import ads

from pre_workbench.consts import WDGEN_HELP_URL
from pre_workbench.errorhandler import check_for_updates
from pre_workbench.guihelper import navigateBrowser, TODO, APP, showWidgetDlg
from pre_workbench.app import NavigateCommands, GlobalEvents
from pre_workbench import configs, consts
# noinspection PyUnresolvedReferences
from pre_workbench import windows
from pre_workbench.configs import getIcon, SettingsSection, SettingsField, icon_searchpaths
from pre_workbench.datawidgets import DynamicDataWidget
from pre_workbench.util import get_app_version, SimpleThread
from pre_workbench.windows.content.objectwindow import ObjectWindow
from pre_workbench.windows.dialogs.manageannotationsets import ManageAnnotationSetsDialog
# noinspection PyUnresolvedReferences
from pre_workbench.windows.dockwindows import FileBrowserWidget, MdiWindowListWidget, StructInfoTreeWidget, \
	StructInfoCodeWidget, DataInspectorWidget, BinwalkDockWidget, ExtToolDockWidget, SearchDockWidget, \
	MacroListDockWidget
from pre_workbench.windows.dockwindows import RangeTreeDockWidget, RangeListWidget, SelectionHeuristicsConfigWidget, LogWidget
from pre_workbench.controls.genericwidgets import MemoryUsageWidget, showPreferencesDlg, showListSelectDialog, \
	showSettingsDlg
from pre_workbench.typeeditor import JsonView
from pre_workbench.typeregistry import WindowTypes, DockWidgetTypes
from pre_workbench.windows.content.hexfile import HexFileWindow

configs.registerOption(SettingsSection('General', 'General', 'Updates', 'Updates'),
							   "CheckForUpdates", "Check for updates on each application start", "check", {}, True, None)

MRU_MAX = 5
class WorkbenchMain(QMainWindow):
	zoom_updated = pyqtSignal(object)
	selected_bytes_updated = pyqtSignal(object)
	grammar_updated = pyqtSignal(object)
	meta_updated = pyqtSignal(str, object)

	def __init__(self, project):
		super().__init__()
		self.project = project
		self.mappedChildActions = list()
		self.activeDocumentMeta = dict()
		self.activeDocumentWindow = None
		self._initUI()
		APP().update_splash("Restoring windows...")
		self.restoreChildren()
		self.mdiArea.restoreState(self.project.getValue("DockState", b""))

		NavigateCommands["WINDOW-ID"] = self.navigateWindowId
		NavigateCommands["WINDOW"] = self.navigateWindow
		NavigateCommands["OPEN"] = self.openFile
		self.statusTimer = QTimer(self)
		self.statusTimer.timeout.connect(self.onStatusTimer)
		self.statusTimer.start(1000)

	def onStatusTimer(self):
		self.statusBar() # TODO was soll das?

	def restoreChildren(self):
		for wndInfo in self.project.getValue("ChildrenInfo", []):
			clz, _ = WindowTypes.find(name=wndInfo["clz"])
			try:
				wnd = clz(**wndInfo["par"])
				wnd.setObjectName(str(wndInfo["id"]))
				self.showChild(wnd)
			except Exception as ex:
				traceback.print_exc()
				msg = QMessageBox(QMessageBox.Critical, "Failed to Restore Window", "Failed to restore window of type "+wndInfo["clz"]+"\n\n"+traceback.format_exc(), QMessageBox.Ok | QMessageBox.Abort, self)
				msg.addButton("Show Parameters", QMessageBox.YesRole)
				res = msg.exec()
				if res == QMessageBox.Abort:
					sys.exit(13)
				if res == 0:
					showWidgetDlg(JsonView(jdata=wndInfo), "Window Parameters", lambda: None, self)
		for wndInfo in self.project.getValue("DockWidgetStates", []):
			try:
				self.dockWidgets[wndInfo["id"]].restoreState(wndInfo["par"])
			except:
				logging.exception("Failed to restore dock widget state for %r", wndInfo["id"])

	def updateChildWindowList(self, obj=None):
		logging.log(logging.TRACE, "updateChildWindowList")
		wndList = self.mdiArea.dockWidgetsMap().values()
		self.dockWidgets["MdiWindowListWidget"].updateWindowList(wndList)

	def closeEvent(self, e):
		configs.setValue("MainWindowGeometry", self.saveGeometry())
		configs.setValue("MainWindowState", self.saveState(123))
		if not self._checkDirtyChildren():
			e.ignore()
			return
		self._saveChildrenState()
		self.project.setValue("DockState", self.mdiArea.saveState())
		super().closeEvent(e)

	def _checkDirtyChildren(self):
		for wnd in self.mdiArea.dockWidgetsMap().values():
			if hasattr(wnd.widget(), "maybeSave"):
				if not wnd.widget().maybeSave():
					logging.info("close cancelled by %r", wnd.widget())
					return False
		return True

	def _saveChildrenState(self):
		self.project.setValue("ChildrenInfo", [
			{
				"id": wnd.widget().objectName(),
				"clz": type(wnd.widget()).__name__,
				"geo": [wnd.pos().x(), wnd.pos().y(), wnd.size().width(), wnd.size().height() ], #bytes(wnd.saveGeometry()),
				"par": wnd.widget().saveParams(),
			}
			for wnd in self.mdiArea.dockWidgetsMap().values()
			if hasattr(wnd.widget(), "saveParams")
		])
		self.project.setValue("DockWidgetStates", [
			{ "id": name, "par": widget.saveState() }
			for name, widget in self.dockWidgets.items()
			if hasattr(widget, "saveState")
		])


	def mapChildAction(self, action, funcName):
		action.setProperty("childFuncName", funcName)
		self.mappedChildActions.append(action)
		action.triggered.connect(self.mappedChildActionTriggered)

	def mappedChildActionTriggered(self):
		funcName = self.sender().property("childFuncName")
		child = self.activeMdiChild()
		if child is not None and hasattr(child, funcName):
			getattr(child, funcName)()
		elif child is not None and hasattr(child, "childActionProxy") and hasattr(child.childActionProxy(), funcName):
			getattr(child.childActionProxy(), funcName)()

	def updateMappedChildActions(self):
		child = self.activeMdiChild()
		if child is None:
			for action in self.mappedChildActions:
				action.setEnabled(False)
		else:
			for action in self.mappedChildActions:
				funcName = action.property("childFuncName")
				action.setEnabled(hasattr(child, funcName) or hasattr(child, "childActionProxy") and hasattr(child.childActionProxy(), funcName))


	def _initActions(self):
		self.exitAct = QAction('Exit', self, shortcut='Ctrl+Q', statusTip='Exit application', triggered=QApplication.closeAllWindows, menuRole=QAction.QuitRole)

		self.openAct = QAction(getIcon('folder-open-document.png'), 'Open', self, shortcut='Ctrl+O',
							   statusTip='Open file', triggered=self.onFileOpenAction)

		self.loadProjectAct = QAction(getIcon('application--plus.png'), 'Open project...', self, shortcut='Ctrl+Shift+O',
							   statusTip='Open project...', triggered=self.onProjectOpenAction)

		self.saveAct = QAction(getIcon('disk.png'), "&Save", self,
				shortcut=QKeySequence.Save,
				statusTip="Save the document to disk")
		self.mapChildAction(self.saveAct, "save")

		self.saveAsAct = QAction(getIcon('disk-rename.png'), "Save &As...", self,
				shortcut=QKeySequence.SaveAs,
				statusTip="Save the document under a new name")
		self.mapChildAction(self.saveAsAct, "saveAs")

		self.reloadFileAct = QAction("&Reload", self,
				shortcut=QKeySequence.Refresh,
				statusTip="Reload the current file from disk")
		self.mapChildAction(self.reloadFileAct, "reloadFile")

		# TODO
		self.closeAct = QAction("Cl&ose", self, shortcut='Ctrl+W',
				statusTip="Close the active window",
				triggered=self.closeActiveChildWindow)

		self.closeAllAct = QAction("Close &All", self, shortcut='Ctrl+Shift+W',
				statusTip="Close all the windows",
				triggered=self.closeAllChildWindows)

		"""self.nextAct = QAction("Ne&xt", self, shortcut=QKeySequence.NextChild,
				statusTip="Move the focus to the next window",
				triggered=self.mdiArea.activateNextSubWindow)

		self.previousAct = QAction("Pre&vious", self,
				shortcut=QKeySequence.PreviousChild,
				statusTip="Move the focus to the previous window",
				triggered=self.mdiArea.activatePreviousSubWindow)"""

		self.reloadGrammarAct = QAction("&Reload grammar", self,
				shortcut="Ctrl+I",
				statusTip="Reload the grammar from disk")
		self.mapChildAction(self.reloadGrammarAct, "reloadGrammar")

		self.clearRangesAct = QAction("&Clear Annotations", self,
				shortcut="Ctrl+Shift+K",
				statusTip="Remove all annotations on the current buffer")
		self.mapChildAction(self.clearRangesAct, "clearRanges")

		self.manageAnnotationSetsAct = QAction("&Manage Annotation Sets", self,
				triggered=lambda: ManageAnnotationSetsDialog(self).exec())

	def _initMenu(self):
		menubar = self.menuBar()
		mainToolbar = self.addToolBar('Main')
		toolWndToolbar = self.addToolBar('Tool Windows')

		##### FILE #####
		fileMenu = menubar.addMenu('&File')
		newTbMenu = fileMenu.addMenu("New Tab")
		for wndTyp, meta in WindowTypes.types:
			text = 'New '+meta.get('displayName', meta.get('name'))
			newAct = QAction(text, self, statusTip=text,
									   triggered=lambda dummy, wndTyp=wndTyp: self.onFileNewWindowAction(wndTyp))
			if wndTyp.__name__ == 'TextFileWindow': newAct.setShortcut('Ctrl+Shift+N')
			if wndTyp.__name__ == 'ObjectWindow': newAct.setShortcut('Ctrl+N')
			#fileMenu.addAction(newAct)
			newTbMenu.addAction(newAct)
		#fileMenu.addAction(self.newAct)

		fileMenu.addAction(self.openAct)
		fileMenu.addAction(self.saveAct)
		fileMenu.addAction(self.saveAsAct)
		fileMenu.addAction(self.reloadFileAct)
		fileMenu.addSeparator()
		#exportMenu = fileMenu.addMenu('&Export')
		#exportMenu.addAction("As &Python Script")
		fileMenu.addSeparator()

		fileMenu.addAction(self.loadProjectAct)
		recentProjectMenu = fileMenu.addMenu('&Recent projects')
		for project in configs.getValue("ProjectMru", []):
			recentProjectMenu.addAction(project, lambda dir=project: self.openProjectInNewWindow(dir))
		fileMenu.addSeparator()

		self.mruActions = []
		for _ in range(MRU_MAX):
			a = fileMenu.addAction("-")
			a.triggered.connect(self.onMruClicked)
			self.mruActions.append(a)
		self.updateMruActions()
		fileMenu.addSeparator()
		fileMenu.addAction(self.exitAct)

		##### VIEW #####
		viewMenu = menubar.addMenu('&View')
		toolWndMenu = viewMenu.addMenu('&Tool Windows')
		for name in self.dockWidgets:
			#a = toolWndMenu.addAction(name, lambda name=name: self.mdiArea.findDockWidget(name).toggleView(True))
			toolWndMenu.addAction(self.mdiArea.findDockWidget(name).toggleViewAction())
			toolWndToolbar.addAction(self.mdiArea.findDockWidget(name).toggleViewAction())
		toolbarsMenu = viewMenu.addMenu('Tool Bars')
		toolbarsMenu.addActions([mainToolbar.toggleViewAction(), toolWndToolbar.toggleViewAction()])
		viewMenu.addSeparator()
		a = QAction("Zoom In", self, shortcut='Ctrl++')
		self.mapChildAction(a, "zoomIn")
		viewMenu.addAction(a)
		a = QAction("Zoom Out", self, shortcut='Ctrl+-')
		self.mapChildAction(a, "zoomOut")
		viewMenu.addAction(a)
		a = QAction("Reset", self, shortcut='Ctrl+0')
		self.mapChildAction(a, "zoomReset")
		viewMenu.addAction(a)

		##### Annotations #####
		annotationsMenu = menubar.addMenu('&Annotations')
		annotationsMenu.addAction(self.clearRangesAct)
		self.loadAnnotationSetMenu = annotationsMenu.addMenu("Load &Annotation Set")
		annotationsMenu.aboutToShow.connect(self._updateParserMenu)
		annotationsMenu.addAction(self.manageAnnotationSetsAct)


		##### PARSER #####
		parserMenu = menubar.addMenu('&Parser')
		parserMenu.addAction(self.reloadGrammarAct)
		self.applyFormatInfoMenu = parserMenu.addMenu("&Parse Buffer")
		parserMenu.aboutToShow.connect(self._updateParserMenu)
		parserMenu.addAction(QAction("Export As Wireshark &Lua Dissector", self, triggered=self.onWiresharkExport))

		##### TOOLS #####
		toolsMenu = menubar.addMenu('&Tools')
		self.macroMenu = toolsMenu.addMenu('&Run Macro')
		self.macroMenu.aboutToShow.connect(self._updateMacroMenu)
		showConfigAction = QAction("Show Raw &Config", self, triggered=lambda: self.showChild(JsonView(jdata=configs.configDict)),
								   shortcut='Ctrl+Shift+,')
		toolsMenu.addAction(showConfigAction)
		editConfigAction = QAction(getIcon("wrench-screwdriver.png"), "&Preferences ...", self, triggered=lambda: self.onPreferences(),
								   menuRole=QAction.PreferencesRole, shortcut='Ctrl+,')
		toolsMenu.addAction(editConfigAction)
		if APP().plugins_dir:
			toolsMenu.addAction(QAction("&Open Plugins Directory", self, triggered=lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(APP().plugins_dir))))
			toolsMenu.addAction(QAction("&Manage Plugins", self, triggered=self.onManagePlugins))

		##### WINDOW #####
		self.windowMenu = menubar.addMenu("&Window")
		self._updateWindowMenu()
		self.windowMenu.aboutToShow.connect(self._updateWindowMenu)

		##### HELP #####
		helpMenu = menubar.addMenu("&Help")
		helpMenu.addAction(QAction("Getting Started", self, triggered=lambda: navigateBrowser(consts.GETTING_STARTED_URL)))
		helpMenu.addAction(QAction("Syntax Reference", self, triggered=lambda: navigateBrowser(consts.SYNTAX_REFERENCE_URL)))
		helpMenu.addAction(QAction("Key Bindings", self, triggered=lambda: navigateBrowser(consts.KEY_BINDINGS_URL)))

		helpMenu.addAction(QAction("Issue Tracker", self, triggered=lambda: navigateBrowser(consts.ISSUE_TRACKER_URL)))
		helpMenu.addSeparator()
		helpMenu.addAction(QAction("About PRE Workbench", self, triggered=lambda: self.showAboutBox(),
								   menuRole=QAction.AboutRole))

		##### MAIN TOOLBAR #####
		newTbAct = QToolButton(self, icon=getIcon('document--plus.png'), text='New', popupMode=QToolButton.InstantPopup)
		newTbAct.setMenu(newTbMenu)
		mainToolbar.addWidget(newTbAct)
		mainToolbar.addAction(self.openAct)
		mainToolbar.addAction(self.saveAct)
		mainToolbar.addAction(self.saveAsAct)
		mainToolbar.addAction(editConfigAction)
		runMacroAction = QToolButton(self, icon=getIcon("scripts.png"), text="Run Macro", popupMode=QToolButton.InstantPopup)
		runMacroAction.setMenu(self.macroMenu)
		mainToolbar.addWidget(runMacroAction)

	def _initDockWindows(self):
		self.dockWidgets = {}

		self.zoomWindow = DynamicDataWidget()
		self.zoomWindow.block_zoom = True # don't forward zoom events from inside the zoom window - causes app crashes
		self.zoomWindow.meta_updated.connect(self.onMetaUpdateRaw)
		self.createDockWnd("Zoom", "Zoom", "document-search-result.png", self.zoomWindow, ads.BottomDockWidgetArea, showFirstRun=True)
		self.zoom_updated.connect(lambda content: self.zoomWindow.setContents(content) if content is not None else None)

		for typ, meta in DockWidgetTypes.types:
			widget = typ()
			self.createDockWnd(meta['name'], meta['title'], meta['icon'], widget, getattr(ads, meta.get('dock', 'Right') + 'DockWidgetArea'), meta.get('showFirstRun', False))
			if hasattr(widget, 'on_meta_updated'): self.meta_updated.connect(widget.on_meta_updated)
			if hasattr(widget, 'on_selected_bytes_updated'): self.selected_bytes_updated.connect(widget.on_selected_bytes_updated)
			if hasattr(widget, 'on_focused_dock_widget_changed'): self.mdiArea.focusedDockWidgetChanged.connect(widget.on_focused_dock_widget_changed)

		self.createDockWnd("Data Source Log", "Data Source Log", "terminal--exclamation.png", LogWidget("DataSource"), ads.TopDockWidgetArea)
		self.createDockWnd("Application Log", "Application Log", "bug--exclamation.png", LogWidget(""), ads.TopDockWidgetArea)

	def _initUI(self):
		ads.CDockManager.setConfigFlag(ads.CDockManager.FocusHighlighting, True)
		ads.CDockManager.setConfigFlag(ads.CDockManager.MiddleMouseButtonClosesTab, True)
		ads.CDockManager.setConfigFlag(ads.CDockManager.AllTabsHaveCloseButton, True)
		ads.CDockManager.setConfigFlag(ads.CDockManager.DockAreaHasCloseButton, False)
		self.mdiArea = ads.CDockManager(self)

		label = QLabel(text="Welcome")
		label.setAlignment(Qt.AlignCenter)
		self.centralDockWidget = ads.CDockWidget("CentralWidget")
		self.centralDockWidget.setWidget(label)
		self.centralDockWidget.setFeature(ads.CDockWidget.NoTab, True)
		self.centralDockWidget.setFeature(ads.CDockWidget.DockWidgetClosable, False)
		self.mdiArea.setCentralWidget(self.centralDockWidget)

		self._initDockWindows()

		self.setUnifiedTitleAndToolBarOnMac(True)
		self.setAcceptDrops(True)

		self.mdiArea.focusedDockWidgetChanged.connect(self.onSubWindowActivated)

		# required for actions in "Window" menu
		self.windowMapper = QSignalMapper(self)
		self.windowMapper.mapped[QWidget].connect(self.setActiveSubWindow)

		self._initActions()
		self._initMenu()

		self.statusBar().addPermanentWidget(MemoryUsageWidget())
		if configs.getValue("General.Updates.CheckForUpdates", True):
			def update_check_result(version):
				if version != get_app_version():
					logging.warning("update_check: A newer version of pre_workbench is available. Installed: "+get_app_version()+", Available: "+version)
					self.statusBar().addPermanentWidget(QPushButton("New Version Available: "+version,
																	styleSheet="QPushButton{background-color:#44ff88;padding:1px 10px;}",
																	clicked=lambda: navigateBrowser(consts.WEBSITE_URL)))
				else:
					logging.info("update_check: Your version of pre_workbench is up to date ("+version+")")
			SimpleThread(self, check_for_updates, update_check_result)
		else:
			logging.warning("update_check: Update check skipped (disabled by user)")

		self.setWindowIcon(getIcon("appicon.png"))
		self.setGeometry(300, 300, 850, 850)
		self.restoreGeometry(configs.getValue("MainWindowGeometry", b""))
		self.restoreState(configs.getValue("MainWindowState", b""), 123)
		self.setWindowTitle(f'PRE Workbench - {self.project.projectFolder}')
		self.setWindowFilePath(self.project.projectDbFile)
		self.show()

	def showAboutBox(self):
		from pre_workbench import errorhandler
		def link(href, prefix=""):
			if href is None: return "None"
			return f"<a href='{prefix}{href}'>{href}</a>"
		showWidgetDlg(QTextBrowser(minimumWidth=520,minimumHeight=300,searchPaths=icon_searchpaths,openLinks=False,anchorClicked=navigateBrowser,
							html="<img src='appicon.png' style='float: left; '><br><b>Protocol Reverse Engineering Workbench</b><br>"
							f"Version {get_app_version()}<br><br>"
							"Copyright (c) 2022 Mira Weller<br>"
							"Licensed under the GNU General Public License Version 3<br style='clear:left'><br><hr>"
							"<table>"
							f"<tr><td>Website: </td><td>{link(consts.WEBSITE_URL)}</td></tr>"
							f"<tr><td>Issue Tracker: </td><td>{link(consts.ISSUE_TRACKER_URL)}</td></tr>"
							"<tr><td>&nbsp;</td><td></td></tr>"
							f"<tr><td>Config Dir: </td><td>{link(configs.dirs.user_config_dir, 'file:')}</td></tr>"
							f"<tr><td>Log File: </td><td>{errorhandler.logFile}</td></tr>"
							f"<tr><td>Plugins Dir: </td><td>{link(APP().plugins_dir, 'file:')}</td></tr>" +
							("<tr><td>Loaded Plugins:</td><td>" + "<br>".join(APP().plugins.keys())+"</td></tr>" if len(APP().plugins) > 0 else "")
							+ "</table>"),
					  "About PRE Workbench", lambda: None, self, buttons=QDialogButtonBox.Close)

	def onPreferences(self):
		res = showPreferencesDlg(configs.configDefinitions, configs.configDict, "Preferences", self)
		if res is not None:
			for k,v in res.items():
				configs.setValue(k,v)
		GlobalEvents.on_config_change.emit()

	def onManagePlugins(self):
		plugins = ["pre_workbench.plugins." + os.path.basename(file)[:-3]
				   for file in glob(os.path.join(APP().plugins_dir, "*.py"))]
		enabled_plugins = configs.getValue("EnabledPlugins", [])
		result = showListSelectDialog(list(zip(plugins, plugins)), enabled_plugins,
									  title="Manage Plugins - Select To Enable",
									  parent=self, multiselect=True, min_width=400)
		if result is not None:
			configs.setValue("EnabledPlugins", result)

	def onWiresharkExport(self):
		from pre_workbench.datasource import formatinfoSelect
		r = showSettingsDlg([
			SettingsField("definition", "Start Grammar Definition", "text", {"listselectcallback":formatinfoSelect}),
			SettingsField("only_types", "Only Export These Definitions", "text", {"listselectcallback":formatinfoSelect,"multiselect":","}),
			SettingsField("dissector_table", "Dissector Table", "text", {}),
			SettingsField("raise_not_implemented", "Raise NotImplementedErrors", "check", {"default":True}),
			SettingsField("output_file", "Output File", "text", {"fileselect":"save","filter":"Lua Script (*.lua)"}),
		], self.project.getValue("LastWiresharkExportOptions", {}), "Wireshark Dissector Export", self, min_width=550,
		help_callback=lambda: navigateBrowser(WDGEN_HELP_URL))
		if r:
			from pre_workbench.wdgen.lua import generate_lua_dissector
			self.project.setValue("LastWiresharkExportOptions", r)
			with open(r['output_file'], 'w') as out:
				generate_lua_dissector(r['definition'], r['only_types'], r['dissector_table'].split(','), self.project.formatInfoContainer, r['raise_not_implemented'], out)
			with open(r['output_file'], 'r') as infile:
				self.zoomWindow.setContents(infile.read())

	def onMruClicked(self):
		self.openFile(self.sender().data())

	def updateMruActions(self):
		mru = configs.getValue("MainFileMru", [])
		for i in range(MRU_MAX):
			self.mruActions[i].setVisible(i < len(mru))
			if i < len(mru):
				self.mruActions[i].setText(os.path.basename(mru[i]))
				self.mruActions[i].setData(mru[i])

	def _updateWindowMenu(self):
		#TODO
		self.windowMenu.clear()
		self.windowMenu.addAction(self.closeAct)
		self.windowMenu.addAction(self.closeAllAct)
		self.windowMenu.addSeparator()
		#self.windowMenu.addAction(self.nextAct)
		#self.windowMenu.addAction(self.previousAct)

		windows = self.getChildWindows()

		for i, window in enumerate(windows):
			child = window.widget()

			text = "%d %s" % (i + 1, window.windowTitle())
			if i < 9:
				text = '&' + text

			action = self.windowMenu.addAction(text)
			action.setCheckable(True)
			action.setChecked(child is self.activeMdiChild())
			action.triggered.connect(self.windowMapper.map)
			self.windowMapper.setMapping(action, window)

	def getChildWindows(self):
		return [wnd for wnd in self.mdiArea.dockWidgetsMap().values() if
				(wnd.features() & ads.CDockWidget.DockWidgetDeleteOnClose) != ads.CDockWidget.NoDockWidgetFeatures]

	def closeActiveChildWindow(self):
		activeSubWindow = self.mdiArea.focusedDockWidget()
		if activeSubWindow:
			activeSubWindow.closeDockWidget()

	def closeAllChildWindows(self):
		for wnd in self.getChildWindows():
			wnd.closeDockWidget()

	def _updateParserMenu(self):
		self.loadAnnotationSetMenu.clear()
		self.applyFormatInfoMenu.clear()
		for name in self.project.getAnnotationSetNames():
			self.loadAnnotationSetMenu.addAction(name, TODO)
		self.loadAnnotationSetMenu.addAction("New...", TODO)

		for name in self.project.formatInfoContainer.definitions.keys():
			self.applyFormatInfoMenu.addAction(name, TODO)
		#menu.addAction("New...", lambda: )

	def _updateMacroMenu(self):
		self.macroMenu.clear()
		for container_id, container, macroName in APP().find_macros_by_input_types(["NONE"]):
			self.macroMenu.addAction(macroName, lambda c=container, name=macroName: c.getMacro(name).execute(None))

	def onSubWindowActivated(self, old: ads.CDockWidget, now: ads.CDockWidget):
		logging.log(logging.TRACE, "onSubWindowActivated")
		self.updateMappedChildActions()
		if now is None or not hasattr(now.widget(), 'child_wnd_meta'): return

		try:
			self.activeDocumentWindow.widget().meta_updated.disconnect(self.onMetaUpdateChild)
		except:
			pass
		self.activeDocumentWindow = now
		try:
			now.widget().meta_updated.connect(self.onMetaUpdateChild)
		except:
			pass

		new_meta = now.widget().child_wnd_meta
		# TODO what about metas only contained in new_meta?
		for ident, oldval in self.activeDocumentMeta.items():
			newval = new_meta.get(ident)
			if newval != oldval:
				self.activeDocumentMeta[ident] = newval
				if hasattr(self, ident+"_updated"): getattr(self, ident+"_updated").emit(newval)
				self.meta_updated.emit(ident, newval)

	def activeMdiChild(self):
		activeSubWindow = self.mdiArea.focusedDockWidget()
		if activeSubWindow:
			return activeSubWindow.widget()
		return None

	def setActiveSubWindow(self, window):
		if window:
			window.toggleView(True)
			window.raise_()
			window.setFocus()
			try:
				window.widget().nextInFocusChain().setFocus()
			except:
				logging.exception("nextInFocusChain")

	def onProjectOpenAction(self):
		self.openProjectInNewWindow()

	def openProjectInNewWindow(self, projectPath = "--choose-project"):
		import subprocess
		self_script = sys.argv[0]
		# weird Windows magic
		if self_script == sys.executable:  # PyInstaller on Windows
			cmd_line = [self_script, projectPath]
		elif not os.path.exists(self_script) and os.path.exists(self_script + '.exe'):  # PIP entry_points on Windows
			cmd_line = [sys.executable, self_script + '.exe', projectPath]
		else:  # everything else
			cmd_line = [sys.executable, self_script, projectPath]
		logging.info('Starting new instance with cmd line: %r', cmd_line)
		subprocess.Popen(cmd_line, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

	def onFileNewWindowAction(self, typ):
		ow = typ()
		self.showChild(ow)

	def onFileOpenAction(self):
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", configs.getValue("lastOpenFile",""))
		if fileName:
			configs.setValue("lastOpenFile", fileName)
			self.openFile(fileName)

	def findWindow(self, Type=None, FileName=None, Id=None):
		for childWnd in self.mdiArea.dockWidgetsMap().values():
			logging.debug("childWnd object name: %s", childWnd.objectName())
			widget = childWnd.widget()
			if ((Type is None or type(widget).__name__ == Type) and
				(FileName is None or (hasattr(widget, "params") and widget.params.get("fileName") == FileName)) and
				(Id is None or childWnd.objectName() == Id)):
				return childWnd

		return None

	def navigateWindowId(self, Id):
		childWnd = self.findWindow(Id=Id)
		if childWnd:
			logging.debug("switching to childWnd: %s", childWnd)
			self.setActiveSubWindow(childWnd)

	@pyqtSlot(str, str)
	def navigateWindow(self, Type, FileName, **kw):
		childWnd = self.findWindow(Type=Type, FileName=FileName)
		if childWnd:
			logging.debug("switching to childWnd: %s", childWnd)
			self.setActiveSubWindow(childWnd)
			return

		winType, _ = WindowTypes.find(name=Type)
		if winType is None:
			QMessageBox.critical(self, "Failed to open window", "Failed to open window of unknown type "+Type)
			return
		try:
			wnd = winType(fileName=FileName, **kw)
			self.showChild(wnd)
		except Exception as ex:
			msg = QMessageBox(QMessageBox.Critical, "Failed to open file", "Failed to open window of type "+winType.__name__+"\n\n"+str(ex), QMessageBox.Ok, self)
			msg.setDetailedText(traceback.format_exc())
			msg.exec()

	@pyqtSlot(str)
	def openFile(self, FileName):
		childWnd = self.findWindow(FileName=FileName)
		if childWnd:
			logging.debug("switching to childWnd: %s", childWnd)
			self.setActiveSubWindow(childWnd)
			return

		configs.updateMru("MainFileMru", FileName, MRU_MAX)
		self.updateMruActions()

		root,ext = os.path.splitext(FileName)
		winType, _ = WindowTypes.find(fileExts=ext)
		if winType is None: winType = ObjectWindow

		try:
			wnd = winType(fileName=FileName)
			self.showChild(wnd)
		except Exception as ex:
			msg = QMessageBox(QMessageBox.Critical, "Failed to open file", "Failed to open window of type "+winType.__name__+"\n\n"+str(ex), QMessageBox.Ok, self)
			msg.setDetailedText(traceback.format_exc())
			msg.exec()

	def onMetaUpdateRaw(self, ident, newval):
		if hasattr(self, ident+"_updated"): getattr(self, ident+"_updated").emit(newval)
		self.meta_updated.emit(ident, newval)

	def onMetaUpdateChild(self, ident, newval):
		self.sender().child_wnd_meta[ident] = newval
		self.activeDocumentMeta[ident] = newval
		if hasattr(self, ident+"_updated"): getattr(self, ident+"_updated").emit(newval)
		self.meta_updated.emit(ident, newval)

	def showChild(self, widget, floating=False):
		logging.debug("showChild %s", widget)
		subwnd = ads.CDockWidget(widget.windowTitle())
		subwnd.setWidget(widget)
		widget.windowTitleChanged.connect(lambda newTitle: subwnd.setWindowTitle(newTitle))
		subwnd.setFeature(ads.CDockWidget.DockWidgetDeleteOnClose, True)
		subwnd.setFeature(ads.CDockWidget.DockWidgetForceCloseWithArea, True)
		subwnd.setWindowIcon(getIcon(type(widget).icon if hasattr(type(widget), 'icon') else 'document.png'))
		widget.child_wnd_meta = dict()
		widget.destroyed.connect(self.updateChildWindowList)
		if not widget.objectName(): widget.setObjectName(str(uuid.uuid1()))
		subwnd.setObjectName(widget.objectName())
		widget.show()
		if floating:
			self.mdiArea.addDockWidgetFloating(subwnd)
		else:
			self.mdiArea.addDockWidgetTabToArea(subwnd, self.centralDockWidget.dockAreaWidget())
		self.updateChildWindowList()

	def createDockWnd(self, name, title, iconName, widget, area=ads.RightDockWidgetArea, showFirstRun=False):
		dw=ads.CDockWidget(title)
		dw.setObjectName(name)
		dw.setWidget(widget)
		dw.setIcon(getIcon(iconName))
		#dw.setToggleViewActionMode(ads.CDockWidget.ActionModeShow)
		dw.toggleViewAction().setIcon(dw.icon())
		self.mdiArea.addDockWidgetTab(area, dw)
		self.dockWidgets[name] = widget
		if not showFirstRun: dw.closeDockWidget()

