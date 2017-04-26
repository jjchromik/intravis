# InTraVis
__In__dustrial __Tra__ffic __Vis__ualizer creates a DTMC and the corresponding graph of a pcap-trace with IEC104 traffic. It was initially designed as a proof of concept for my bachelor thesis -- Sequence attacks on SCADA networks. 

It can also export the resulting DTMC in XML format. Uppon the corresponding DTMC two minimizations(bisimulations) are supported. The first minimization merges all IOAs together, the second merges states with overlapping IOAs together. 

__NOTE__: This tool has been intended for research purpose. 

## Usage
usage: __init__.py [-h] -t FILE -i IPs [-o OUTPUTFILE] [-x OUTPUTFILE]
                   [-b BISIMULATION] [-c] [-v FILE]

description of the program

optional arguments:
  -h, --help       show this help message and exit
  -t FILE          train the DTMC with this file
  -i IPs           two IPs semi-colon seperated
  -o OUTPUTFILE    pdf outputfile
  -x OUTPUTFILE    xml outputfile
  -b BISIMULATION  use bisimulation. "0": no bisimulation(default), "1": merge
                   all IOAS, "2": merge overlapping IOAs
  -c               colored graph
  -v FILE          validate this trace against the training trace

## Requirements
1. pyshon3.x
2. pyshark

