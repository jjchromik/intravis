from .transition import Transition
import hashlib

class State():

	def __init__(self, cff, req, res, typeId, asduAddress, ioas, dateTime, bisimulation):
		"""
		:param cff: single letter {I, U, S}
		:param req: bool
		:param res: bool
		:param typeId: int
		:param asduAddress: int
		:param ioa: str
		:param dateTime: int
		:return:
		"""
		""" count of the events carrying the same information """
		self.numberEvents = 1
		
		""""""
		self.controlFieldFormat = cff
		
		""""""		
		self.request = req
		
		""""""			
		self.response = res
		
		""""""	
		self.typeId = typeId
		
		""""""	
		self.asduAddress = asduAddress
		
		""""""	
		self.ioas = ioas
		
		""" first occurance of the event """
		self.firstTimeSeen = dateTime

		""" last occurance of the event """
		self.lastTimeSeen = dateTime

		""" """
		self.transitions = []

		""" """
		self.totalJumps = 0
		
		""" entry state"""
		self.entry = False
		
		self.bisimulation = bisimulation
		
		self.violation = False

	def update(self, dateTime, ioas=[]):
		self.numberEvents += 1
		self.lastTimeSeen = dateTime
		
		if len(ioas) == 0:
			return
			
		if(self.bisimulation == 2):
			for n in ioas:
				if n not in self.ioas:
					self.ioas.append(n)
		
	def mergeTransitions(self):
		merged = True
		while merged:
			merged = False
			for pTransition in self.transitions:
				for oTransition in self.transitions:
					if id(pTransition) == id(oTransition):
						continue
					if id(pTransition.destination) == id(oTransition.destination):
						pTransition.destinationJumps += oTransition.destinationJumps
						self.deleteTransition(oTransition)
						merged = True
						break
				if merged:
					break
	
	def deleteTransition(self, transition):
		index = 0
		for t in self.transitions:
			if id(transition) == id(t):
				del self.transitions[index]
				return
			index += 1
		
	def entryState(self, entry):
		self.entry = entry
	
	def jump(self, destination, dateTime):		
		self.totalJumps += 1
		transition = Transition(self, destination, dateTime)
		if transition in self.transitions:
			# transition already exists
			index = self.transitions.index(transition)
			self.transitions[index].update(dateTime)
		else:
			# transition does not exist
			self.transitions.append(transition)

	def __eq__(self, other):
		if self.bisimulation == 1:
			return self.__bisimulationEq__(other)
		elif self.bisimulation == 2:
			return self.__bisimulationEq2__(other)
		return self.__defaultEq__(other)

	def __defaultEq__(self, other):
		return ((self.controlFieldFormat == other.controlFieldFormat) and
			(self.request == other.request) and
			(self.response == other.response) and
			(self.typeId == other.typeId) and
			(self.ioas == other.ioas) and
			(self.asduAddress == other.asduAddress))

	def __bisimulationEq__(self, other):
		return ((self.controlFieldFormat == other.controlFieldFormat) and
			(self.request == other.request) and
			(self.response == other.response) and
			(self.typeId == other.typeId) and
			(self.asduAddress == other.asduAddress))

	def __bisimulationEq2__(self, other):
		overlap = False
		for ioa in self.ioas:
			for ioa_other in other.ioas:
				if ioa == ioa_other:
					overlap = True
					break
			if overlap:
				break
		return ((self.controlFieldFormat == other.controlFieldFormat) and
			(self.request == other.request) and
			(self.response == other.response) and
			(self.typeId == other.typeId) and
			(overlap) and
			(self.asduAddress == other.asduAddress))

	def __hash__(self):
		if self.bisimulation == 1:
			return self.__bisimulationHash__()
		elif self.bisimulation == 2:
			''' default hash can be used as well, since the IOAs are partially merged. '''
			return self.__defaultHash__()
		return self.__defaultHash__()
	
	def __defaultHash__(self):
		hash = hashlib.md5(str(str(self.controlFieldFormat) + 
			str(self.request) + 
			str(self.response) + 
			str(self.typeId) + 
			str(self.ioas) +
			str(self.asduAddress)).encode() )
		hex = hash.hexdigest()
		return int(hex, 16)	
	
	def __bisimulationHash__(self):
		hash = hashlib.md5(str(str(self.controlFieldFormat) + 
			str(self.request) + 
			str(self.response) + 
			str(self.typeId) + 
			str(self.asduAddress)).encode() )
		hex = hash.hexdigest()
		return int(hex, 16)	
	
	def __str__(self):
		return str("CFF: " + str(self.controlFieldFormat) + 
			" -- REQ: " + str(self.request) + 
			" -- RES: " + str(self.response) + 
			" -- TypeID: " + str(self.typeId) + 
			" -- IOA: " + str(self.ioas) +
			" -- ASDU: " + str(self.asduAddress))