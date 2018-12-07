#!/Users/joshj55/anaconda/bin/python2.7

##Created by: Josh Jones, D. Sarah Stamps
##Date last modified: 5 Dec 2018
##This script is the parsing section of the UNAVCO -> CHORDS workflow
##includes connections to nclient_beta, UNAVCO caster and chords_stream
##Please read the README.txt before starting

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
import chords_stream

#function that parses the strings for latitude and longitude.
#Requires string,direction as input which are read from the input file and contained in the path read
def parse_string(string,direction):
	string_val= map(str,string)
	string_test=string.split('.')
	string_deg= string_val[0]
#These statements find the degrees and minutes in the latitude/longitude for the difference in decimal places 1., 10., and 100.
	if len(string_test[0]) == 3:
		string_deg= string_val[0]
		string_min= string_val[1]+string_val[2]
	elif len(string_test[0]) == 4:
		string_deg= string_val[0]+string_val[1]
		string_min= string_val[2]+string_val[3]
	elif len(string_test[0]) == 5:
		string_deg= string_val[0]+string_val[1]+string_val[2]
		string_min= string_val[3]+string_val[4]
	string_sec= string_test[1]
	string_min_sec= float(string_min+'.'+string_sec)/60
	string_full=float(string_deg)+string_min_sec
#writes the directions as + or - based off of if the latitude/longitude is E/N or W/S| Necessary for CHORDS
	if direction == 'E' or 'N':
		string_final= string_full
	elif direction == 'W' or 'S':
		string_final= -1 * string_full
	return string_final


#Pareses the time field read from the input file and place it into CHORDS format hr/min/sec
def parse_time(time):
	time_string= map(str,time)
	time_split= time.split('.')
	time_front=time_split[0]
	time_hour= time_front[0]+time_front[1]
	time_min= time_front[2]+time_front[3]
	time_sec= time_front[4:]
	time_fin= str(time_hour)+':'+str(time_min)+':'+str(time_sec)
	return time_fin


#Parses the data read from the input file and places it into CHORDS format yr/mon/day
def parse_date(date):
	date_string= map(str,date)
	date_mon= date_string[0]+date_string[1]
	date_day= (date_string[2])+(date_string[3])
	date_yr= date_string[4]+date_string[5]
	date_fin= str(20)+str(date_yr)+'-'+str(date_mon)+'-'+str(date_day)
	return date_fin


#Reads the input file and takes the information to be parse
def read_file(filename):
	path= open(filename, "r")
	read_path= path.readline()
	path.close()
	path= open(filename, "r+")
	new_path= path.readlines()
	updated_path= new_path[1:]
	new_path.insert(0,updated_path)
	path.close()
	path= open(filename, "w")
	path.writelines(updated_path)
	path.close()
	return read_path


#Runs the above function and splits the read line from the input file by commas and assign them to variables for the functions
if __name__=='__main__':
	filename="chords_temp_data.txt"
	myline= read_file(filename).split(',')
	time= myline[2]
	date= myline[3]
	latitude_string= myline[4]
	latitude_dir= myline[5]
	longitude_string= myline[6]
	longitude_dir= myline[7]
	latitude_final = parse_string(latitude_string,latitude_dir)
	longitude_final= parse_string(longitude_string,longitude_dir)
	time_final= parse_time(time)
	date_final= parse_date(date)
	height= str(myline[11])[3:]
	site_id= 8
	date_fin = datetime.utcnow().strftime("%Y-%m-%d")
	time_fin = datetime.utcnow().strftime("%H:%M:%S")
	url = 'http://tzvolcano.chordsrt.com/measurements/url_create?instrument_id='+str(site_id)+'&lat='+str(latitude_final)+'&lon='+str(longitude_final)+'&height='+str(height)+'at='+str(date_final)+'T'+time_final
	response=requests.get(url=url)

