from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from datetime import date

class XMLWriter():
	
	def __init__(self, dtmc):
		self.dtmc = dtmc
		self.timeFormat = '%Y-%m-%d %H:%M:%S'

	def createXml(self, filename):
		""" DTMC properties """
		id = str(self.dtmc.__hash__())
		createDate = self.dtmc.states[1].firstTimeSeen.strftime(self.timeFormat)
		desc = "Discrete-Time Markov Chain Model"
		firstEvent = self.dtmc.states[1].firstTimeSeen.strftime(self.timeFormat)
		lastEvent = self.dtmc.states[len(self.dtmc.states)-1].firstTimeSeen.strftime(self.timeFormat)
		
		""" State properties """
		numOfStates = str(len(self.dtmc.states))
		numOfEvents = 0
		for s in self.dtmc.states:
			numOfEvents += s.numberEvents
		
		""" Transition properties """
		numOfJumps = 0
		for s in self.dtmc.states:
			for t in s.transitions:
				numOfJumps += t.destinationJumps
		numOfTransitions = 0
		for s in self.dtmc.states:
			for t in s.transitions:
				numOfTransitions += 1
		
		
		dtmc = Element('Dtmc', Id=str(id), Created=str(createDate), Description=str(desc), FirstEvent=str(firstEvent), LastEvent=str(lastEvent))
		states = SubElement(dtmc, 'States', NumberOfStates=str(numOfStates), NumberOfEvents=str(numOfEvents))
		transitions = SubElement(dtmc, 'Transitions', NumberOfTransitions=str(numOfTransitions), NumberOfJumps=str(numOfJumps))

		for s in self.dtmc.states:
			id = s.__hash__()
			a = SubElement(states, 'State', Id=str(id))
			firstTimeSeen = s.firstTimeSeen.strftime(self.timeFormat)
			lastTimeSeen = s.lastTimeSeen.strftime(self.timeFormat)
			SubElement(a, 'Attributes', Name=str(id), Data=str(s), FirstTimeHere=firstTimeSeen, LastTimeHere=lastTimeSeen, NumberOfEvents=str(s.numberEvents))
			for t in s.transitions:
				firstJump = t.firstJump.strftime(self.timeFormat)
				lastJump = t.lastJump.strftime(self.timeFormat)
				b = SubElement(transitions, "Transition", Id=str(id))
				SubElement(b, "Endpoints", Src=str(t.source.__hash__()), Dst=str(t.destination.__hash__()))
				SubElement(b, "Attributes", Name="", Data="", FirstTime=firstJump, LastTime=lastJump, AvgTimeElapsed=str(t.medianTime), StdDeviationTimeElapsed=str(t.calcStdDeviation()), SumTimeElapsed_support="1", SumPowTimeElapsed_support="1", NumberOfJumps=str(t.destinationJumps), ProbabilityOfTransition=str(t.calcTransitionProbability()))
		
		output_file = open( filename, 'w' )
		output_file.write( '<?xml version="1.0" encoding="UTF-8"?>' )
		output_file.write( ElementTree.tostring(dtmc).decode('utf-8') )
		output_file.close()		
		
		