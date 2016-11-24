import math
import hashlib

class Transition():
	"""
	represents the transition described in the paper
	"""

	def __init__(self, source, destination, dateTime):
		"""
			:param destination: destination State
			:param dateTime: dateTime of the packet
			"""

		""" source state """
		self.source = source

		""" destination state """
		self.destination = destination

		""" dateTime of first occurance of a transition from source to destination """
		self.firstJump = dateTime

		""" dateTime of last occurance of a transition from source to destination """
		self.lastJump = dateTime

		""" total number of jumps from source to destination """
		self.destinationJumps = 1

		""" standard deviation if the time intervals between two jumps """
		self.stdDeviation = 0

		""" ratio: destinationJumps / source.totalJumps """
		self.transitionPropability = 0

		""" list of time intervals between two consecutive jumps """
		self.timeGaps = []

		""" average time of the time intervals between two jumps """
		self.medianTime = 0
		
		self.violation = False

	def update(self, dateTime):
		"""
		:param dateTime:
		:return:
		"""
		self.timeGaps.append(dateTime - self.lastJump)
		self.lastJump = dateTime
		self.destinationJumps += 1
		
	def updateBisimilar(self, transition):
		if self.lastJump <= transition.lastJump:
			self.lastJump = transition.lastJump
		if self.firstJump > transition.firstJump:
			self.firstJump = transition.firstJump
		#for timeGap in transition.timeGaps:
			#self.timeGaps.append(timeGap)

	def transitionProbability(self):
		"""
		:return:
		"""
		return str(self.destinationJumps) + "/" + str(self.source.totalJumps) + "\n" + str(round((self.destinationJumps/self.source.totalJumps), 3))
	
	def calcTransitionProbability(self):
		return self.destinationJumps/self.source.totalJumps

	def calcStdDeviation(self):
		"""
			return: standard deviation 
		"""
		sum = 0
		for gap in self.timeGaps:
			sum += gap.total_seconds()
			
		var = sum/self.destinationJumps
		return math.sqrt(var)

	def getMedianTime(self):
		"""
			return average time between two jumps
		"""
		return round((self.lastJump - self.firstJump) / self.destinationJumps, 3)

	def __eq__(self, other):
		# eq if source and destination equals
		return ((self.source == other.source) and
			(self.destination == other.destination))

	def __hash__(self):
		hash = hashlib.md5(str(self.source + self.destination).encode())
		hex = hash.hexdigest()
		return int(hex, 16)
