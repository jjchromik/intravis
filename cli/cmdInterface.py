import graph
import parser
import sys

class Cli():
	"""
	represents the command line interface
	"""	
	
	def __init__(self, arguments):
		ips = str(arguments.ips).split(';')
		self.ip1 = ips[0]
		self.ip2 = ips[1]
		self.colored = arguments.colored
		self.trainingTrace = arguments.trainingTrace
		self.testingTrace = arguments.testingTrace
		self.bisimulation = int(arguments.bisimulation)
		self.outputXml = arguments.outputxml

		pdffilename = arguments.outputpdf.rstrip('pdf').rstrip('.')
		self.outputPdf = pdffilename
		
		if not self.testingTrace == "":
			self.colored = False
		
	def run(self):
		if self.testingTrace == "":
			dtmc = self.createDTMC(self.trainingTrace, int(self.bisimulation))
			
		else:
			trainingDtmc = self.createDTMC(self.trainingTrace, self.bisimulation)
			testingDtmc = self.createDTMC(self.testingTrace, self.bisimulation)
			testingDtmc.validate(trainingDtmc)
			dtmc = testingDtmc
			
		if not self.outputPdf == "":
			self.createPdf(dtmc, self.outputPdf)
			
		if not self.outputXml == "":
			self.createXml(dtmc, self.outputXml)
			
		return 0
	
	def createDTMC(self, trace, bisimulation):
		Cli.cprint('creating DTMC...')
		iec104Parser = parser.PcapParser(trace, self.ip1, self.ip2, bisimulation)
		dtmc = iec104Parser.parsePcap()
		Cli.cprintnl('done')
		return dtmc
	
	def createPdf(self, dtmc, filename):
		Cli.cprint('generating pdf file(' + filename + '.pdf)...')
		g = graph.Graph(dtmc)
		g.generate_graph(filename, self.colored)
		Cli.cprintnl('done')
		
	def createXml(self, dtmc, filename):
		Cli.cprint('generating xml file(' + filename + ')...')
		xmlwriter = graph.XMLWriter(dtmc)
		xmlwriter.createXml(filename)
		Cli.cprintnl('done')
	
	def cprint(msg):
		print(msg, end='')
		sys.stdout.flush()
	
	def cprintnl(msg):
		print(msg)
		sys.stdout.flush()
	