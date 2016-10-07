from graphviz import Digraph
import os
from datetime import datetime

class Graph():
	"""
	represents the graph
	"""	

	def __init__(self, dtmc):
		self.timeFormat = '%Y-%m-%d %H:%M:%S'
		self.dtmc = dtmc
		self.edges = []
		self.nodes = {}
		self.graph = Digraph(graph_attr={"rankdir":"RLRTRL"})
		self.maxJumpRate = 0
		for state in dtmc.states:
			if self.maxJumpRate < state.totalJumps:
				self.maxJumpRate = state.totalJumps
		
	def generate_graph(self, outputfile, colored=False):
		if colored:
			self.colored_graph()
		else:
			self.mono_graph()
			
		self.graph.render(outputfile)
		os.remove(outputfile)			
	
	def mono_graph(self):
		for state in self.dtmc.states:
			self.addTransitions(id(state), state.transitions)
			
			if state.entry:
				self.nodes.update({id(state): "ENTRY"})
				continue

			direction = self.nameDirection(state)
			firstOccurance = state.firstTimeSeen.strftime(self.timeFormat)
			lastOccurance = state.lastTimeSeen.strftime(self.timeFormat)
			self.nodes.update({id(state): "ID: " + str(state.__hash__()) + "\n" +
				"Direction: " + direction + 
				" -- Type: " + str(state.controlFieldFormat) + 
				" -- TypeID: " + str(state.typeId) + 
				"\nASDU-Addr: " + str(state.asduAddress) +
				"\nIOA: " + str(state.ioas) + 
				#"\nFirst occurance: " + str(firstOccurance) + 
				#"\nLast occurance: " + str(lastOccurance) +
				"\nCount: " + str(state.numberEvents)})
			
		for node in self.nodes:
			self.graph.node(str(node), str(self.nodes[node]), {'penwidth' : "7"})
	
		for edge in self.edges:
			self.graph.edge(str(edge[0]), str(edge[1]), str(edge[2]), edge[3])					
	
	def colored_graph(self):
		colors = ['blue', 'brown', 'yellow', 'green', 'cyan', 'orange', 'purple', 'darkgreen', 'teal', 'magenta']
		nodeHashes = {}
		nodeColors = []

		for state in self.dtmc.states:
			self.addTransitions(id(state), state.transitions)
				
			if state.entry:
				self.nodes.update({id(state): "ENTRY"})
				nodeHashes.update({id(state) : str(state.__bisimulationHash__())})
				if str(nodeHashes[id(state)]) not in nodeColors:
					nodeColors.append(nodeHashes[id(state)])
				continue
			
			direction = self.nameDirection(state)	
			
			firstOccurance = state.firstTimeSeen.strftime(self.timeFormat)
			lastOccurance = state.lastTimeSeen.strftime(self.timeFormat)	
			ioas = "["
			i = 0
			for ioa in state.ioas:
				i += 1
				if i % 10 == 0:
					ioas += "\n"
				ioas += "'" + str(ioa) + "',"
			ioas = ioas.strip(",")
			ioas += "]"
			self.nodes.update({id(state): #"ID: " + str(state.__hash__()) + "\n" +
				# "B_ID: " + str(state.__bisimulationHash__()) + "\n" +
				"Direction: " + direction + 
				" --- " + str(state.controlFieldFormat) +
				" -- TypeID: " + str(state.typeId) + 
				"\nASDU-Addr: " + str(state.asduAddress) +
				"\nIOA(s): " + str(ioas) + 
				#"\nFirst occurance: " + str(firstOccurance) + 
				#"\nLast occurance: " + str(lastOccurance) +
				"\nCount: " + str(state.numberEvents)})
			nodeHashes.update({id(state) : str(state.__bisimulationHash__())})
			if str(nodeHashes[id(state)]) not in nodeColors:
				nodeColors.append(nodeHashes[id(state)])
				
		for node in self.nodes:
			self.graph.node(str(node), str(self.nodes[node]), {'color' : colors[ nodeColors.index( str(nodeHashes[node]) ) % len(colors)-1 ], 'penwidth' : "7", "rotate":"90", "fontsize":"24pt"})	
	
		for edge in self.edges:
			self.graph.edge(str(edge[0]), str(edge[1]), str(edge[2]), edge[3])
	
	def addTransitions(self, stateId, transitions):
		for transition in transitions:
			self.edges.append((stateId, id(transition.destination), " " + transition.transitionProbability(), {'penwidth' : str(int(7*transition.destinationJumps/self.maxJumpRate+1)), "fontsize":"24pt"}))
			
	def nameDirection(self, state):
		direction = ""

		if state.request == 1 and state.response == 1:
			direction = "REQ+RES"
		elif state.request == 1:
			direction = "REQ"
		elif state.response == 1:
			direction = "RES"

		return direction
	