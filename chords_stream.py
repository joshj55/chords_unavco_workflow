#!/Users/joshj55/anaconda/bin/python2.7

##Created by: Josh Jones, D. Sarah Stamps
##Date last modified: 5 Dec 2018
##This script is the streaming section of the UNAVCO -> CHORDS workflow
##includes connections to nclient_beta, UNAVCO caster and chords_parse
##Please read the README.txt file before starting

from __future__ import print_function
import socket
import sys
import psutil 
from datetime import datetime
import base64
import requests
import time
import os
import subprocess
import argparse
import json
import pprint
import nclient_beta
import chords_parse
import chords_background

def execute(cmd):
	"""Runs the chords_background script that activates the UNAVCO caster in the background."""

	output= subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
	for stdout_line in iter(output.stdout.readline, ""):
		yield stdout_line
	output.stdout.close()
	return_code = output.wait()
	if return_code:
		raise subprocess.CalledProcessError(return_code,cmd)


def write_file(filename,write_line):
	"""#Function that writes the data coming in from the UNAVCO caster subprocess."""

	open_file= open(filename, "a")
	open_file.write(str(write_line))
	return filename

def getargs(argv):
	"""Parse the command line arguments.

	Keyword arguments:
	argv -- the command line argument vector
	The arguments are returned as the argparse dictionary.
	"""

	description = 'Stream UNVACO GNSS to CHORDS.'
	epilog = """
The json file is structured as
follows (order is not important):
{
  "caster_ip":   "caster IP name",
  "caster_user": "caster user name",
  "caster_pw":   "caster password",
  "chords_ip":   "CHORDS portal IP name",
  "chords_key":  "CHORDS portal data ingest key",
  "sites": [
    "1st caster site identifier",
    "2nd caster site identifier",
    ...
    "nth caster site identifier"
  ]
}
"""
	parser = argparse.ArgumentParser(description=description, epilog=epilog,
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument(
		'-j', '--json', metavar='file', action='store',type=str,
						help='json configuration file', required=True)
	args = parser.parse_args()

	args_dict = vars(args)
	jsonfile = args_dict['json']
	if not os.access(jsonfile, os.R_OK):
		print("Configuration file", jsonfile,"is not readable.")
		exit(1)

	return args_dict

def getoptions(config_file):
	"""Return the configuration file options as a dictionary."""
	
	j = json.load(open(config_file))
	return j

if __name__=='__main__':
	"""Main block of code that repeats a connection request until connection with UNAVCO caster is made."""
	args = getargs(argv=sys.argv)
	options = getoptions(args['json'])
	print(options)

	filename="chords_temp_data.txt"
	data_flow = 0
	while data_flow == 0:
		for path in execute(['python','./chords_background.py']):
			if 'Unauthorized' in path:
				data_flow= 0
			elif '$' in path:
				data_flow= 1
				write_line= path
				write_file(filename,write_line)
				execfile("./chords_parse.py")

