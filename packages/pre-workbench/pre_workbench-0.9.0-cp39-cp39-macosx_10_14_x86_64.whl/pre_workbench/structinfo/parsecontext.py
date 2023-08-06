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
import struct
from typing import Optional, Any, Dict

from pre_workbench.algo.range import Range

from pre_workbench.objects import ByteBufferList, ByteBuffer
from pre_workbench.structinfo.exceptions import *
from pre_workbench.structinfo.expr import Expression
from pre_workbench.structinfo.hexdump import hexdump


class FormatInfoContainer:
	def __init__(self, definitions: Optional[Dict[str, Any]] = None, load_from_file: Optional[str] = None, load_from_string: Optional[str] = None):
		self.definitions = {} if definitions is None else definitions
		self.definition_comments = {}
		self.main_name = None
		self.file_name = None
		if load_from_file is not None: self.load_from_file(load_from_file)
		if load_from_string is not None: self.load_from_string(load_from_string)

	def to_text(self, indent = 0):
		return "\n\n".join((self.definition_comments[name]+"\n" if self.definition_comments.get(name) else "") + name+" "+value.to_text(indent, None) for name, value in self.definitions.items())

	def load_from_file(self, fileName):
		if fileName.endswith(".txt"):
			with open(fileName, "r") as f:
				self.load_from_string(f.read())
		else:
			with open(fileName, "rb") as f:
				#return bin_deserialize_fi(f.read())
				#TODO
				raise NotImplemented
		self.file_name = fileName

	def load_from_string(self, txt):
		from pre_workbench.structinfo.parser import parse_definition_map_into_container
		self.definitions = {}
		self.definition_comments = {}
		parse_definition_map_into_container(txt, self)

	def write_file(self, fileName):
		if fileName.endswith(".txt"):
			txt = self.to_text()
			with open(fileName, "w") as f:
				f.write(txt)
		elif fileName.endswith(".pfi"):
			#ser = bin_serialize_fi(fi)
			#with open(fileName, "wb") as f:
			#	f.write(ser)
			raise NotImplemented
		else:
			raise Exception("unsupported file type")

	def get_fi_by_def_name(self, def_name):
			return self.definitions[def_name]

class stack_frame:
	__slots__ = ('desc', 'value', 'id', 'buf_offset', 'buf_limit_end')

	def __init__(self, desc, value, id, buf_offset, buf_limit_end):
		self.desc = desc
		self.value = value
		self.id = id
		self.buf_offset = buf_offset
		self.buf_limit_end = buf_limit_end


class ParseContext:
	logger = logging.getLogger("DataSource")

	def __init__(self, format_infos: FormatInfoContainer, buf: bytes = None, logging_enabled=False):
		self.format_infos = format_infos
		self.stack = list()
		self.id = ""
		self.buf_offset = 0
		self.buf_limit_end = None
		self.display_offset_delta = 0
		self.buf = bytes()
		self.on_new_subflow_category = None
		self.subflow_categories = dict()
		self.failed = None
		self.logging_enabled = logging_enabled
		if buf is not None:
			self.feed_bytes(buf)

	def set_failed(self, ex: parse_exception):
		if not isinstance(ex, parse_exception):
			raise TypeError("Argument to set_failed must be of type parse_exception")
		self.failed = ex
		self.log("Marking context as failed", str(ex))

	def clear_failed(self):
		self.failed = None
		self.log("Resetting context failed")

	def hexdump_context(self, ptr: int, context: int = 16):
		start = ptr - (ptr%16) - context
		end = start + 2*context
		return hexdump(self.buf[start - self.display_offset_delta : end - self.display_offset_delta], result='return', addr_offset=start, addr_ptr=ptr-start)

	def get_fi_by_def_name(self, def_name: str):
		try:
			return self.format_infos.get_fi_by_def_name(def_name)
		except KeyError:
			raise parse_exception(self, "reference to undefined formatinfo name: "+def_name)

	def feed_bytes(self, data):
		remove_bytes = self.buf_offset if len(self.stack) == 0 else 0
		self.buf = self.buf[remove_bytes:] + data
		self.display_offset_delta += remove_bytes
		self.buf_offset -= remove_bytes
		if self.buf_limit_end != None:
			self.buf_limit_end -= remove_bytes

	def parse(self, by_name: Optional[str] = None):
		if by_name is None: by_name = self.format_infos.main_name
		self.id = by_name
		result = self.get_fi_by_def_name(by_name).read_from_buffer(self)
		if self.failed:
			ParseContext.logger.exception("Failed to parse", exc_info=self.failed)
			#self.failed.partial_result = result
			#raise self.failed
		return result

	def get_param(self, id: str, default = None, raise_if_missing: bool = True):
		for i in range(len(self.stack)-1, -1, -1):
			if hasattr(self.stack[i].desc, 'params'):
				if id in self.stack[i].desc.params:
					return self.stack[i].desc.params[id]
		if raise_if_missing:
			raise value_not_found(self, "Missing parameter "+id)
		else:
			return default

	def push(self, desc, value = None, id: Optional[str] = None):
		if id != None: self.id = id
		self.log("push", desc)
		self.stack.append(stack_frame(desc, value, self.id, self.buf_offset, self.buf_limit_end))
		self.id=""

	def restore_offset(self):
		self.buf_offset = self.stack[-1].buf_offset

	def pop(self):
		self.log("pop")
		frame = self.stack.pop()
		self.id = frame.id; self.buf_limit_end = frame.buf_limit_end
		self.log("-->", frame.value, frame.desc)
		return frame.value

	def set_child_limit(self, max_length: int):
		self.require_bytes(max_length)
		self.buf_limit_end = self.buf_offset + max_length

	def get_path(self, delim="."):
		return delim.join(frame.id for frame in self.stack)

	def log(self, *dat):
		if not self.logging_enabled: return
		try:
			ParseContext.logger._log(logging.INFO, "%s: %s", (self.get_path(), "\t".join(str(x) for x in dat)))
		except Exception as ex:
			ParseContext.logger.exception( self.get_path() + ": EXCEPTION IN LOGGING")

	def remaining_bytes(self):
		if self.buf_limit_end:
			return self.buf_limit_end - self.buf_offset
		else:
			return len(self.buf) - self.buf_offset

	def require_bytes(self, needed: int):
		if self.remaining_bytes() < needed: raise incomplete(self, needed, self.remaining_bytes())

	def peek_structformat(self, format_string: str):
		return struct.unpack_from(self.get_param('endianness') + format_string, self.buf, self.buf_offset)

	def peek_int(self, n: int, signed: bool):
		return int.from_bytes(self.buf[self.buf_offset:self.buf_offset+n], signed=signed, byteorder='little' if n == 1 or self.get_param('endianness') == '<' else 'big')

	def peek_bytes(self, n: int):
		return self.buf[self.buf_offset : self.buf_offset + n]

	def consume_bytes(self, count: int):
		self.require_bytes(count)
		self.buf_offset += count

	def read_bytes(self, count: int):
		self.require_bytes(count)
		self.buf_offset += count
		return self.buf[self.buf_offset - count:self.buf_offset]

	def offset(self):
		return self.buf_offset + self.display_offset_delta

	def top_offset(self, stack_index: int = -1):
		return self.stack[stack_index].buf_offset + self.display_offset_delta

	def top_length(self, stack_index: int = -1):
		return self.buf_offset - self.stack[stack_index].buf_offset + self.display_offset_delta

	def top_value(self, stack_index: int = -1):
		return self.stack[stack_index].value

	def top_id(self):
		for i in reversed(range(len(self.stack))):
			id = self.stack[i].id
			if id: return id
		return None

	def set_top_value(self, value):
		self.stack[-1].value = value

	def top_buf(self, stack_index: int = -1):
		return self.buf[ self.stack[stack_index].buf_offset : self.buf_offset ]

	def pack_value(self, value):
		self.log("pack(L)",type(self.stack[-1].desc).__name__, self.top_offset(), self.top_length())#, value)
		if self.on_new_subflow_category is not None and hasattr(self.stack[-1].desc, 'params'):
			try:
				desc = self.stack[-1].desc
				if 'reassemble_into' in desc.params:
					category, meta, subflow_key = self.build_subflow_key(desc.params['reassemble_into'])
					print("reassemble:",category,subflow_key,value)
					new = False
					if category not in self.subflow_categories:
						self.subflow_categories[category] = ByteBufferList()
						new = True
					databytes = self.top_buf()
					if 'segment_meta' in desc.params:
						datameta = { k: v.evaluate(self) for k,v in desc.params['segment_meta'] }
					else:
						datameta = {}
					self.subflow_categories[category].reassemble(subflow_key, meta, databytes, datameta)
					if new: self.on_new_subflow_category(category=category, parse_context=self)

				if 'store_into' in desc.params:
					category, meta, subflow_key = self.build_subflow_key(desc.params['store_into'])
					print("store:",category,subflow_key,value)
					new = False
					if category not in self.subflow_categories:
						self.subflow_categories[category] = ByteBufferList()
						new = True
					self.subflow_categories[category].add(ByteBuffer(buf=self.top_buf(), metadata=meta))
					if new: self.on_new_subflow_category(category=category, parse_context=self)

			except Exception as ex:
				raise parse_exception(self, "while adding bytes to reassembly buffer: "+ str(ex)) from ex

		return value

	def pack_error(self, ex):
		return None

	def unpack_value(self, packed_value):
		return packed_value

	def build_subflow_key(self, param: list):
		meta = {}
		category = param[0]
		subflow_key = []
		for expr in param[1:]:
			if isinstance(expr, Expression):
				key, value = expr.expr_str, expr.evaluate(self)
			else:
				key, value = str(expr), str(expr)
			meta[key] = value
			subflow_key.append(value)
		return category, meta, tuple(subflow_key)


class AnnotatingParseContext(ParseContext):
	def pack_value(self, value):
		from pre_workbench.structinfo.format_info import FormatInfo
		source_desc = self.stack[-1].desc
		self.log("pack(A)",type(source_desc).__name__, self.top_offset(), self.top_length())#, value)
		range = Range(self.top_offset(), self.top_offset() + self.top_length(), super().pack_value(value), source_desc=source_desc, field_name=str(self.top_id()))
		range.metadata.update({ 'name': self.get_path(), 'pos': self.top_offset(), 'size': self.top_length(), '_sdef_ref': source_desc, 'show': str(value) })

		if isinstance(source_desc, FormatInfo):
			range.metadata.update(source_desc.extra_params(context=self))
		elif isinstance(source_desc, dict):
			range.metadata.update(source_desc)
		return range

	def pack_error(self, ex):
		range = self.pack_value(None)
		range.exception = ex
		return range

	def unpack_value(self, packed_value):
		while isinstance(packed_value, Range):
			packed_value = packed_value.value
		return packed_value
