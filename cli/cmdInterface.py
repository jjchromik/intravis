import ids
import graph
import parser
import sys

class Cli():
	"""
	represents the command line interface
	"""	
	
	def __init__(self, cleanFile, ip1, ip2, colored=False):
		self.cleanFile = cleanFile
		self.ip1 = ip1
		self.ip2 = ip2
		self.dtmc = 0
		self.colored = colored
		self.pdfFile = ''
		self.xmlFile = ''
	
	def createDTMC(self, bisimulation):
		Cli.cprint('creating DTMC...')
		iec104Parser = parser.PcapParser(self.cleanFile, self.ip1, self.ip2, bisimulation)
		self.dtmc = iec104Parser.parsePcap()
		Cli.cprintnl('done')
	
	def createPdf(self, filename=''):
		outputFile = self.pdfFile
		if not filename == '' :
			outputFile = filename
		Cli.cprint('generating pdf file...')
		g = graph.Graph(self.dtmc)
		g.generate_graph(outputFile, self.colored)
		Cli.cprintnl(outputFile + '.pdf created.')
		
	def createXml(self):
		Cli.cprint('generating xml file...')
		xmlwriter = graph.XMLWriter(self.dtmc)
		xmlwriter.createXml(self.xmlFile)
		Cli.cprintnl(self.xmlFile + ' created.')
	
	def cprint(msg):
		print(msg, end='')
		sys.stdout.flush()
	
	def cprintnl(msg):
		print(msg)
		sys.stdout.flush()
	
	def setXmlFile(self, filename):
		self.xmlFile = filename
		
	def setPdfFile(self, filename):
		self.pdfFile = filename
	