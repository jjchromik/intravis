from .transition import Transition
import cli

class DTMC():
	"""
	represents the ids
	"""

	def __init__(self, entry, bisimulation):
		"""
		:return:
		"""
		self.bisimulation = bisimulation
		
		""" set of states """
		self.states = []
		""" initial state - entry point"""
		self.states.append(entry)

		""" last saved state """
		self.lastState = entry

	def addState(self, state):
		timestamp = state.lastTimeSeen
		if state in self.states:
			# get the real object
			tmpstate = state
			state = self.states[self.states.index(state)]
			if(self.bisimulation != 0):
				state.update(timestamp, tmpstate.ioas)
			else:
				state.update(timestamp)	
		else:
			self.states.append(state)
		
		self.lastState.jump(state, timestamp)
		self.lastState = state	
	
	def minimize(self):
		while self.merge() == True:
			print(".", end="")
		print()
		
	def merge(self):
		for persistentState in self.states:
			for obsoleteState in self.states:
				if persistentState.__eq__(obsoleteState) == False:
					continue
				''' check if the !equal! states are in reality one state '''
				if id(persistentState) == id(obsoleteState):
					continue
				''' persistentState and obsoleteState are equal '''
				self.mergeStates(persistentState, obsoleteState)
				
				return True
		return False
		
	def mergeStates(self, persistentState, obsoleteState):
		''' update general attributes '''
		persistentState.totalJumps += obsoleteState.totalJumps
		persistentState.numberEvents += obsoleteState.numberEvents
		
		''' update transitions '''
		for transition in obsoleteState.transitions:
			if (id(transition.destination) == id(persistentState)) or (id(transition.destination) == id(obsoleteState)):
				# from obsolete to persistent --> add/update persistent self loop
				# from obsolete to obsolete --> add/update persistent self loop
				update = False
				for pTransition in persistentState.transitions:
					if id(pTransition.destination) == id(persistentState):
						# update
						pTransition.destinationJumps += transition.destinationJumps
						update = True
				if update == False:
					# add
					transition.source = persistentState
					transition.destination = persistentState
					persistentState.transitions.append(transition)
			else:
				# from obsolete to any other --> add/update persistent transitions
				update = False
				for pTransition in persistentState.transitions:
					if id(pTransition.destination) == id(transition.destination):
						# update
						pTransition.destinationJumps += transition.destinationJumps
						update = True
				if update == False:
					# add
					transition.source = persistentState
					persistentState.transitions.append(transition)
		
		# from any state to obsoleteState --> redirect to persistentState
		for state in self.states:
			if id(state) == id(obsoleteState):
				continue
				
			for transition in state.transitions:
				if id(transition.destination) == id(obsoleteState):
					transition.destination = persistentState
			
			state.mergeTransitions()
		
		''' update IOAs '''
		for ioa in obsoleteState.ioas:
			if ioa not in persistentState.ioas:
				persistentState.ioas.append(ioa)
				persistentState.ioas.sort()
				
		''' remove obsoleteState '''
		self.removeState(obsoleteState)
	
	def removeState(self, state):
		index = 0
		for st in self.states:
			if id(state) == id(st):
				del self.states[index]
				return
			index += 1
	
	def validate(self, dtmc):
		"""
		validate this dtmc against a potential clean training dtmc
		"""
		for state in self.states:
			state.violation = True
			if state in dtmc.states:
				state.violation = False
			for transition in state.transitions:
				if transition.source.entry:
					continue
				transition.violation = True
				for cleanState in dtmc.states:
					if transition in cleanState.transitions:
						transition.violation = False			
		
		stateViolations = 0
		transitionViolations = 0
		for state in self.states:
			if state.violation:
				stateViolations += 1
			for transition in state.transitions:
				if transition.violation:
					transitionViolations += 1
				
		cli.Cli.cprintnl("State violations: " + str(stateViolations))				
		cli.Cli.cprintnl("Transition violations: " + str(transitionViolations))
		
		
		return 0