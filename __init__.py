#!/usr/bin/env python3
import argparse	
import sys
import re
import ids

if __name__ == "__main__":
	''' initialize the argparser '''
	parser = argparse.ArgumentParser(description='description of the program', epilog='written by Benedikt Ferling<benedikt.ferling@wwu.de>')

	parser.add_argument("-t", dest='inputtrace', metavar="FILE", required=True, help='teaching the DTMC with this file')
	parser.add_argument("-i", dest='ips', metavar="IPs", required=True, help='two IPs semi-colon seperated')	
	parser.add_argument("-o", dest='outputpdf', metavar="OUTPUTFILE", help='pdf outputfile')
	parser.add_argument("-x", dest='outputxml', metavar="OUTPUTFILE", help="xml outputfile")
	parser.add_argument("-b", dest='bisimulation', metavar="BISIMULATION", default=0, help='use bisimulation. "0": no bisimulation(default), "1": merge all IOAS, "2": merge overlapping IOAs')
	parser.add_argument("-c", dest='colored', action="store_true", default=False, help='colored graph')
	
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(0)
	
	args = parser.parse_args()
	
	import cli
	if not args.outputpdf and not args.outputxml:
		parser.print_help()
		exit(1)
		
	if not args.ips:
		parser.print_help()
		exit(1)
		
	ips = str(args.ips).split(';')
	c = cli.Cli(args.inputtrace, ips[0], ips[1], args.colored)
	c.createDTMC(int(args.bisimulation))
	
	if args.outputpdf:
		tmp = args.outputpdf.rstrip('pdf')
		filename = tmp.rstrip('.')
		c.setPdfFile(filename)
		c.createPdf()
		
	if args.outputxml:
		tmp = args.outputxml.rstrip('xml')
		filename = tmp.rstrip('.')
		c.setXmlFile(filename)
		c.createXml()
		
	exit(0)