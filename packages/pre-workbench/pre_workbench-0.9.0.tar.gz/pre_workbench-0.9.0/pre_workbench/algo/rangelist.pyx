from collections import defaultdict
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
	from pre_workbench.algo.range import Range

cdef class RangeList:
	cdef list ranges
	cdef list chunks
	cdef int chunkSize
	cdef int chunkCount
	cdef dict annotationStartCache
	cdef dict annotationContainsCache

	def __init__(self, int totalLength, list ranges not None, int chunkSize = 128):
		cdef int firstChunk, lastChunk, i
		self.ranges = ranges
		self.annotationStartCache = dict()
		self.annotationContainsCache = dict()
		self.chunkCount = totalLength // chunkSize + 1
		self.chunkSize = chunkSize
		self.chunks = [[] for i in range(self.chunkCount)]
		for el in ranges:
			firstChunk = el.start // chunkSize
			lastChunk = el.end // chunkSize
			for i in range(firstChunk, lastChunk+1):
				self.chunks[i].append(el)

	def invalidateCaches(self):
		self.annotationStartCache = dict()
		self.annotationContainsCache = dict()

	cdef void _cacheMetaValuesStart(self, str metaKey) except *:
		indizes = defaultdict(list)
		for el in self.ranges:
			if el.metadata.get(metaKey) is not None:
				indizes[el.start].append(el.metadata[metaKey])
		self.annotationStartCache[metaKey] = indizes

	def getMetaValuesStartingAt(self, int start, str metaKey not None):
		if not metaKey in self.annotationStartCache: self._cacheMetaValuesStart(metaKey)
		return self.annotationStartCache[metaKey][start]

	cdef void _cacheMetaValuesContains(self, str metaKey) except *:
		cdef int index
		indizes = defaultdict(list)
		for el in self.ranges:
			if el.metadata.get(metaKey) is not None:
				for index in range(el.start, el.end):
					indizes[index].append(el.metadata[metaKey])
		self.annotationContainsCache[metaKey] = indizes

	def getMetaValuesContaining(self, int start, str metaKey not None):
		if not metaKey in self.annotationContainsCache: self._cacheMetaValuesContains(metaKey)
		return self.annotationContainsCache[metaKey][start]

	def findMatchingRanges(self,
						   start: Optional[int]=None,
						   end: Optional[int]=None,
						   contains: Optional[int]=None,
						   overlaps: Optional[Range]=None,
						   containsRange: Optional[Range]=None, **kw):
		cdef int scanChunk = -1
		if start is not None:
			scanChunk = start // self.chunkSize
		elif end is not None:
			scanChunk = end // self.chunkSize
		elif contains is not None:
			scanChunk = contains // self.chunkSize
		elif overlaps is not None:
			firstChunk = overlaps.start // self.chunkSize
			lastChunk = overlaps.end // self.chunkSize
			if firstChunk == lastChunk:
				scanChunk = firstChunk
		elif containsRange is not None:
			scanChunk = containsRange.start // self.chunkSize

		if scanChunk != -1:
			if scanChunk >= self.chunkCount: return
			for el in self.chunks[scanChunk]:
				if el.matches(start=start, end=end, contains=contains, overlaps=overlaps, containsRange=containsRange, **kw):
					yield el
		else:
			for el in self.ranges:
				if el.matches(start=start, end=end, contains=contains, overlaps=overlaps, containsRange=containsRange, **kw):
					yield el

	def __len__(self):
		return len(self.ranges)

	def append(self, el):
		cdef int firstChunk = el.start // self.chunkSize
		cdef int lastChunk = el.end // self.chunkSize
		cdef int i
		while lastChunk >= self.chunkCount:
			self.chunks.append(list())
			self.chunkCount += 1
		for i in range(firstChunk, lastChunk+1):
			self.chunks[i].append(el)
		self.ranges.append(el)

	def remove(self, el):
		cdef int firstChunk = el.start // self.chunkSize
		cdef int lastChunk = el.end // self.chunkSize
		cdef int i
		for i in range(firstChunk, lastChunk+1):
			self.chunks[i].remove(el)
		self.ranges.remove(el)


