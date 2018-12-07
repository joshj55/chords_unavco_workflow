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
from optparse import OptionParser
import nclient_beta
import chords_parse

#Runs the chords_background script that activates the UNAVCO caster in the background
def execute(cmd):	
	output= subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
	for stdout_line in iter(output.stdout.readline, ""):
		yield stdout_line
	output.stdout.close()
	return_code = output.wait()
	if return_code:
		raise subprocess.CalledProcessError(return_code,cmd)


#Function that writes the data coming in from the UNAVCO caster subprocess 
def write_file(filename,write_line):
	open_file= open(filename, "a")
	open_file.write(str(write_line))
	return filename


#Main block of code that repeats a connection request until connection with UNAVCO caster is made 
if __name__=='__main__':
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

