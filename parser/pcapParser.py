import ids
import pyshark
from datetime import datetime

class PcapParser():
	
	def __init__(self, filename, ip1, ip2, bisimulation=0):
		self.filename = filename
		self.ip1 = ip1
		self.ip2 = ip2
		self.bisimulation = bisimulation
		
		entryDate = datetime.fromtimestamp(0)
		entryState = ids.State("-", False, False, 0, 0, [], entryDate, bisimulation)
		entryState.entryState(True)
		self.dtmc = ids.DTMC(entryState, bisimulation)
		self.states = []
		self.iec104Port = 2404
	
	""""""
	def parsePcap(self):
		capture = pyshark.FileCapture(self.filename)		
		for p in capture:
			self.parsePacket(p)
		
		if self.bisimulation == 2:
			self.dtmc.minimize()
			
		return self.dtmc
		
	""""""
	def parsePacket(self, p):	
		request = False
		response = False
		packetStates = []
		
		if not self.isAsduPacket(p):
			return
		
		if not self.checkIp(p):
			return
		
		timestamp = self.getTimestamp(p)
		
		""" determine direction from TCP-Layer"""
		request = self.isRequest(p)
		response = self.isResponse(p)
		if not (request or response):
			return
		
		for layer in range(len(p.layers)-1):
			if not (self.isApciLayer(p[layer])):
				continue
			
			cff = self.getControlFieldFormat(p[layer])

			""" type id (reading, writing, ...)"""
			typeId = str(p[layer+1].typeid)
	
			""" ASDU-address (common address)"""
			asduAddress = str(p[layer+1].addr)
	
			""" IOA (information object address)"""
			ioas = self.getIoas(p[layer+1])
			
			state = ids.State(cff, request, response, typeId, asduAddress, ioas, timestamp, self.bisimulation)
			self.dtmc.addState(state)
		
	def getIoas(self, layer):
		ioas = []
		ioas.append(layer.ioa)
		for field in layer._get_all_fields_with_alternates():
			if str(field).find("104asdu.ioa") != -1:
				ioas.append(field.show)
		return ioas
	
	def isAsduPacket(self, p):
		if str(p.layers).find("ASDU") != -1:
			return True
		return False
	
	def isApciLayer(self, layer):
		if "104apci" in layer.layer_name:
			return True
		return False
	
	def getTimestamp(self, p):
		timeEpoch = str(p.frame_info.time_epoch).split('.')
		dt = datetime.fromtimestamp(int(timeEpoch[0]))
		return dt
		
	def checkIp(self, p):
		""" only consider the communication between one host and one client"""
		if str(p.layers).find("IP Layer") != -1:
			ips = [p['ip'].src, p['ip'].dst]
			if (self.ip1 in ips and self.ip2 in ips):
				return True	
		return False		
	
	def isRequest(self, p):
		""" is packet a request? """
		if p['TCP'].srcport == str(self.iec104Port):
			return True
		return False
	
	def isResponse(self, p):
		""" is packet a response? """
		if p['TCP'].dstport == str(self.iec104Port):
			return True
		return False
		
	def getControlFieldFormat(self, layer):
		""" Type of {I, S, U} (nummeric values)"""
		if layer._all_fields['104apci.type'] == "0":
			return "I"
		if layer._all_fields['104apci.type'] == "1":
			return "S"
		if layer._all_fields['104apci.type'] == "3":
			return "U"
	