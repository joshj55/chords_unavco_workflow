#!/Users/joshj55/anaconda/bin/python2.7

##Created by: Josh Jones, D. Sarah Stamps
##Date last modified: 5 Dec 2018
##This script is the parsing section of the UNAVCO -> CHORDS workflow
##includes connections to nclient_beta, UNAVCO caster, and chords_stream
##Please read the README.txt before starting

import socket
import sys
import datetime
import base64
import time
import os
import subprocess
from optparse import OptionParser
import nclient_beta

#function where the UNAVCO caster parameters are set.
def func_site():
	user='-u joshj55:ZxBIQ4K2'
	caster='rtgpsout.unavco.org'
	port='2110'
	site='AC20_RTX'
	site_test='AB53_RTX'
	return user, caster, port, site

#seperates the parameters set in the above function as options needed for the UNAVCO client.
if __name__=='__main__':	
	options = func_site()
	o0=options[0]
	o1=options[1]
	o2=options[2]
	o3=options[3]
	cmd='./nclient_beta.py '+ o0 +' '+ o1 +' '+ o2+' ' + o3
	os.system(cmd)

