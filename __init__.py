#!/usr/bin/env python3
import argparse	
import sys
import re
import cli

if __name__ == "__main__":
	''' initialize the argparser '''
	parser = argparse.ArgumentParser(description='', epilog='written by Benedikt Ferling<benedikt.ferling@wwu.de>')

	parser.add_argument("-t", dest='trainingTrace', metavar="FILE", required=True, help='train the DTMC with this file')
	parser.add_argument("-i", dest='ips', metavar="IPs", required=True, help='two IPs semi-colon seperated')	
	parser.add_argument("-o", dest='outputpdf', metavar="OUTPUTFILE", default="", help='pdf outputfile')
	parser.add_argument("-x", dest='outputxml', metavar="OUTPUTFILE", default="", help="xml outputfile")
	parser.add_argument("-b", dest='bisimulation', metavar="BISIMULATION", default=0, help='use bisimulation. "0": no bisimulation(default), "1": merge all IOAS, "2": merge overlapping IOAs')
	parser.add_argument("-c", dest='colored', action="store_true", default=False, help='colored graph')
	parser.add_argument("-v", dest='testingTrace', default="", metavar="FILE", help='validate this trace against the training trace')
	
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(0)
		
	args = parser.parse_args()
	
	if args.outputpdf == "" and args.outputxml == "":
		parser.print_help()
		exit(1)
		
	cli = cli.Cli(args)
	exitcode = cli.run()
	
	exit(exitcode)
