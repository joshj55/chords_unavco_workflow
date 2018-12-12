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

verbose = False

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
	"""Function that writes the data coming in from the UNAVCO caster subprocess."""

	open_file= open(filename, "a")
	open_file.write(str(write_line))
	return filename

def get_args(argv):
	"""Parse the command line arguments.

	Keyword arguments:
	argv -- the command line argument vector

	The arguments are returned as the argparse dictionary.
	"""

	description = 'Stream UNVACO GNSS to CHORDS.'
	epilog = """
The json file is structured as follows (order is not important):
{
  "caster_ip":   "caster IP name",
  "caster_port": "caster port number",
  "caster_user": "caster user name",
  "caster_pw":   "caster password",
  "chords_ip":   "CHORDS portal IP name",
  "chords_key":  "CHORDS portal data ingest key",
  "sites": [
    {"caster_site": "1st caster site", "chords_inst_id": "chords instrument id"},
    ...
    {"caster_site": "nth caster site", "chords_inst_id": "chords instrument id"}
  ]
}
Set chords_key to an empty string if it is not required.
"""

	global verbose
	parser = argparse.ArgumentParser(description=description, epilog=epilog,
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument(
		'-j', '--json', metavar='file', action='store',type=str,
						help='json configuration file', required=True)
	parser.add_argument(
		'-v', '--verbose', action='store_true', default=False,
						help='enable debug printing')

	args = parser.parse_args()

	args_dict = vars(args)

	# Was an accesible configuration file specified?
	jsonfile = args_dict['json']
	if not os.access(jsonfile, os.R_OK):
		print("Configuration file", jsonfile,"is not readable.")
		exit(1)

	# Enable/disable verbosity
	verbose = args_dict['verbose']

	return args_dict

def get_options(config_file):
	"""Return the configuration file options as a dictionary."""
	
	j = json.load(open(config_file))

	if verbose:
		pprint.pprint(j)

	return j

def run_nclient(options):
	""" Run nclient as a subprocess, returning data lines via yield.

	Keyword arguments:
	options -- a dictionary containing the json configuration file options.
	"""

	user    = options['caster_user']
	pw      = options['caster_pw']
	port    = options['caster_port']
	ip      = options['caster_ip']
	site    = options['sites'][0]["caster_site"]

	cmd = ['python', './nclient_beta.py', '-u', user+":"+pw, ip, port, site]
	if verbose:
		print(cmd)
	output = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
	for line in iter(output.stdout.readline, ""):
		line = line.strip()
		yield line
	output.stdout.close()
	return_code = output.wait()
	if return_code:
		raise subprocess.CalledProcessError(return_code,cmd)

if __name__=='__main__':
	"""Main block of code that repeats a connection request until connection with UNAVCO caster is made."""
	
	# Get the command line arguments.
	args = get_args(argv=sys.argv)
	
	# Get the configuration options
	options = get_options(args['json'])

	chords_ip = options['chords_ip']
	chords_inst_id = options['sites'][0]['chords_inst_id']
	chords_key = None
	if options['chords_key'] != '':
		chords_key = options['chords_key']

	# Run nclient, and feed the data lines to CHORDS
	for gnss_line in run_nclient(options):
		if 'Unauthorized' in gnss_line:
			print('Authentication to', options['caster_ip']+':'+options['caster_port'], 'failed for user', options['caster_user'])
			exit(1)
		if gnss_line[0] == '$':
			if verbose:
				print(gnss_line)
			chords_parse.send_to_chords(
				gnss_line=gnss_line, 
				chords_ip=chords_ip, 
				chords_key=chords_key,
				chords_inst_id=chords_inst_id, verbose=verbose)
		else:
			print('Unrecognized line returned from caster:', gnss_line)
