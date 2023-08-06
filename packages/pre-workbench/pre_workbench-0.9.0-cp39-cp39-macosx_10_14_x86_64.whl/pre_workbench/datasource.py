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
import base64
import re

import binascii
import glob
import logging
import os

from PyQt5.QtCore import (pyqtSignal, QObject, QProcess)

from pre_workbench.bbuf_parsing import apply_grammar_on_bbuf
from pre_workbench.configs import SettingsField, SettingsSection, registerOption, getValue
from pre_workbench.guihelper import APP
from pre_workbench.objects import ByteBuffer, ByteBufferList, ReloadRequired
from pre_workbench.structinfo.exceptions import invalid, incomplete
from pre_workbench.structinfo.pcap_reader import read_pcap_file, PcapFormats
from pre_workbench.typeregistry import TypeRegistry
from pre_workbench.tshark_helper import findTshark, PdmlToPacketListParser, findInterfaces
from pre_workbench.util import PerfTimer

group = SettingsSection('DataSources', 'Data Sources', 'wireshark', 'Wireshark Integration')
try:
	tsharkDefault = findTshark()
except FileNotFoundError:
	tsharkDefault = ""
registerOption(group, "tsharkBinary", "tshark Binary", "text", {"fileselect":"open"}, tsharkDefault, None)

DataSourceTypes = TypeRegistry()


class DataSource(QObject):
	on_finished = pyqtSignal()
	logger = logging.getLogger("DataSource")
	def __init__(self, params):
		super().__init__()
		self.params = params
	def updateParam(self, key, value):
		raise ReloadRequired()
	def startFetch(self):
		pass
	def cancelFetch(self):
		pass


class SyncDataSource(DataSource):
	def startFetch(self):
		obj = self.process()
		self.on_finished.emit()
		return obj

	def cancelFetch(self):
		pass


class MacroDataSource(SyncDataSource):
	def __init__(self, macro_container_id, macroname, params):
		super().__init__(params)
		self.macro_container_id = macro_container_id
		self.macroname = macroname
	def process(self):
		macro = APP().get_macro(self.macro_container_id, self.macroname)
		return macro.execute(None, self.params)


@DataSourceTypes.register(DisplayName="Binary file")
class FileDataSource(SyncDataSource):
	@staticmethod
	def getConfigFields():
		return [
			SettingsField("fileName", "File name", "text", {"fileselect": "open"}),
			SettingsField("formatInfo", "Grammar definition", "text", {"listselectcallback":formatinfoSelect})
		]

	def process(self):
		bbuf = ByteBuffer(metadata={'fileName': self.params['fileName'],
									'fileTimestamp': os.path.getmtime(self.params['fileName'])})
		with open(self.params['fileName'], "rb") as f:
			bbuf.setContent(f.read())

		apply_grammar_on_bbuf(bbuf, self.params["formatInfo"])
		return bbuf


@DataSourceTypes.register(DisplayName="Directory of binary files")
class DirectoryOfBinFilesDataSource(SyncDataSource):
	@staticmethod
	def getConfigFields():
		return [
			SettingsField("fileName", "Directory", "text", {"fileselect": "dir"}),
			SettingsField("filePattern", "Search pattern", "text", {"default":"*"}),
			SettingsField("formatInfo", "Grammar definition", "text", {"listselectcallback":formatinfoSelect})
		]

	def process(self):
		globStr = self.params['fileName'] + '/' + self.params['filePattern']
		plist = ByteBufferList()
		for fileName in sorted(glob.glob(globStr)):
			if not os.path.isfile(fileName): continue
			bbuf = ByteBuffer(metadata={'fileName': os.path.basename(fileName),
										'fileTimestamp': os.path.getmtime(fileName)})
			with open(fileName, "rb") as f:
				bbuf.setContent(f.read())

			apply_grammar_on_bbuf(bbuf, self.params["formatInfo"])

			plist.add(bbuf)

		return plist


@DataSourceTypes.register(DisplayName = "CSV file")
class CSVFileDataSource(SyncDataSource):
	@staticmethod
	def getConfigFields():
		return [
			SettingsField("fileName", "File name", "text", {"fileselect":"open"}),
			SettingsField("csvDelimiter", "CSV column delimiter", "text", {"default":","}),
			SettingsField("csvQuoteChar", "CSV quote character", "text", {"default":"\""}),
			SettingsField("csvHeaders", "CSV file contains header", "check", {"default":True}),
			SettingsField("payloadColumnIdx", "Payload column index", "text", {"listselectcallback": CSVFileDataSource._headerSelect}),
			SettingsField("payloadEncoding", "Payload encoding", "select", {"options":[("hex","hex"),("base64","base64"),]}),
			SettingsField("formatInfo", "Grammar definition", "text", {"listselectcallback":formatinfoSelect}),
		]

	@staticmethod
	def _headerSelect(dialog):
		import csv
		with open(dialog.values['fileName'], "r") as csvfile:
			reader = csv.reader(csvfile, delimiter=dialog.values['csvDelimiter'], quotechar=dialog.values['csvQuoteChar'])
			header = next(reader)
			return ((str(i), f) for i, f in enumerate(header))

	def _getPayloadDecoder(self):
		if self.params['payloadEncoding'] == "hex":
			return binascii.unhexlify
		elif self.params['payloadEncoding'] == "base64":
			return base64.b64decode

	def _prepareMeta(self, row, headers):
		if headers:
			return dict(zip(headers, row))
		else:
			return {"col%d" % i: field for i, field in enumerate(row)}

	def process(self):
		import csv
		plist = ByteBufferList()
		decoder = self._getPayloadDecoder()
		payload_idx = int(self.params['payloadColumnIdx'])
		with open(self.params['fileName'], "r") as csvfile:
			reader = csv.reader(csvfile, delimiter=self.params['csvDelimiter'], quotechar=self.params['csvQuoteChar'])
			try:
				header = next(reader) if self.params['csvHeaders'] else None
			except Exception as exc:
				raise Exception("Failed to read header") from exc
			for i, row in enumerate(reader):
				try:
					payload = re.sub("\s", "", row[payload_idx])
					payload_decoded = decoder(payload)
					plist.add(ByteBuffer(payload_decoded, metadata=self._prepareMeta(row, header)))
				except IndexError as exc:
					raise Exception("Failed to read row %d: can't decode payload at index %d because row only has %d columns" % (i, payload_idx, len(row))) from exc
				except Exception as exc:
					raise Exception("Failed to read row %d" % i) from exc

		for bbuf in plist.buffers:
			apply_grammar_on_bbuf(bbuf, self.params["formatInfo"])

		return plist


@DataSourceTypes.register(DisplayName = "PCAP file")
class PcapFileDataSource(SyncDataSource):
	@staticmethod
	def getConfigFields():
		return [
			SettingsField("fileName", "File name", "text", {"fileselect":"open"}),
			SettingsField("formatInfo", "Grammar definition", "text", {"listselectcallback":formatinfoSelect})
		]

	def process(self):
		with PerfTimer('Load PCAP file'):
			with open(self.params['fileName'], "rb") as f:
				plist = read_pcap_file(f)

		with PerfTimer('Parse Buffers'):
			for bbuf in plist.buffers:
				apply_grammar_on_bbuf(bbuf, self.params["formatInfo"])

		return plist



class AbstractTsharkDataSource(DataSource):
	def startFetch(self):
		self.plist = ByteBufferList()
		self.process = QProcess()
		self.process.finished.connect(self.onProcessFinished)
		self.process.readyReadStandardError.connect(self.onReadyReadStderr)
		self.process.readyReadStandardOutput.connect(self.onReadyReadStdout)

		self.process.start(getValue("DataSources.wireshark.tsharkBinary"), self.getArgs())
		self.target=PdmlToPacketListParser(self.plist)
		return self.plist

	def onReadyReadStderr(self):
		self.logger.warning("STD-ERR FROM Tshark: %s", self.process.readAllStandardError().data().decode("utf-8", "replace"))

	def onReadyReadStdout(self):
		self.plist.beginUpdate()
		self.target.feed(self.process.readAllStandardOutput())
		self.plist.endUpdate()

	def onProcessFinished(self, exitCode, exitStatus):
		self.on_finished.emit()

	def cancelFetch(self):
		self.process.terminate()
		self.process.waitForFinished(500)
		self.process.kill()


@DataSourceTypes.register(DisplayName = "PCAP file via Tshark")
class TsharkPcapFileDataSource(AbstractTsharkDataSource):
	@staticmethod
	def getConfigFields():
		return [
			SettingsField("fileName", "File name", "text", {"fileselect":"open"}),
			SettingsField("displayFilter", "Display filter", "text", {}),
			SettingsField("decodeAs", "Decode as", "text", {})
		]

	def getArgs(self):
		args = ["-r", self.params["fileName"], "-T", "pdml"]
		if self.params["displayFilter"] != "":
			args += ["-Y", self.params["displayFilter"]]
		if self.params["decodeAs"] != "":
			args += ["-d", self.params["decodeAs"]]
		return args


@DataSourceTypes.register(DisplayName = "Live capture via Tshark")
class TsharkLiveDataSource(AbstractTsharkDataSource):
	@staticmethod
	def getConfigFields():
		return [
			SettingsField("interface", "Interface", "select", {"options":findInterfaces()}),
			SettingsField("captureFilter", "libpcap-style capture filter", "text", {}),
			SettingsField("displayFilter", "Display filter", "text", {}),
			SettingsField("decodeAs", "Decode as", "text", {}),
		]

	def getArgs(self):
		args = ["-i", self.params["interface"], "-T", "pdml"]
		if self.params["captureFilter"] != "":
			args += ["-f", self.params["captureFilter"]]
		if self.params["displayFilter"] != "":
			args += ["-Y", self.params["displayFilter"]]
		if self.params["decodeAs"] != "":
			args += ["-d", self.params["decodeAs"]]
		return args


@DataSourceTypes.register(DisplayName = "Live capture via PCAP over stdout")
class LivePcapCaptureDataSource(DataSource):
	@staticmethod
	def getConfigFields():
		return [
			SettingsField("shell_cmd", "Shell command line", "text", {"default":"sudo tcpdump -w -"})
		]

	def startFetch(self):
		self.plist = ByteBufferList()
		self.packetFI = None
		from pre_workbench.structinfo.parsecontext import ParseContext
		self.ctx = ParseContext()
		self.process = QProcess()
		self.process.finished.connect(self.onProcessFinished)
		self.process.readyReadStandardError.connect(self.onReadyReadStderr)
		self.process.readyReadStandardOutput.connect(self.onReadyReadStdout)

		self.process.start("/bin/sh", ["-c", self.params["shell_cmd"]])

		return self.plist

	def tryParseHeader(self):
		for headerFI, packetFI in PcapFormats:
			try:
				header = headerFI.read_from_buffer(self.ctx)
				self.packetFI = packetFI
				self.plist.metadata.update(header)
				return
			except invalid as ex:
				self.logger.debug("invalid pcap format, trying next (exception: %r)", ex)
		raise invalid(self.ctx, "no PcapVariant matched")

	def onReadyReadStderr(self):
		self.logger.warning("STD-ERR: %s", self.process.readAllStandardError().data().decode("utf-8", "replace"))

	def onReadyReadStdout(self):
		self.ctx.feed_bytes(self.process.readAllStandardOutput())
		try:
			if self.packetFI is None:
				self.tryParseHeader()
			while True:
				packet = self.packetFI.read_from_buffer(self.ctx)
				self.plist.add(ByteBuffer(packet['payload'], metadata=packet['header']))
		except incomplete:
			return
		except invalid as ex:
			self.logger.exception("Invalid packet format - killing pcap")
			self.cancelFetch()

	def onProcessFinished(self, exitCode, exitStatus):
		self.on_finished.emit()

	def cancelFetch(self):
		self.process.terminate()
		self.process.waitForFinished(500)
		self.process.kill()

def formatinfoSelect(dialog):
	names = APP().project.formatInfoContainer.definitions.keys()
	return zip(names, names)
