This is the README file with information and instructions for the suite of scripts used to access UNAVCO Real-Time Data stream and upload parsed data to the online cybertool CHORDS.
Creator: Josh Jones, D. Sarah Stamps
Institution: Virginia Tech
Last Date Modified: 5 Dec 2018
# Introduction

The following are the scripts provided and required for the main code to run (chords_stream.py), but note the actual instructions are below for running the code:

## chords_stream.py

Main code that executes the others. Starts the UNAVCO data stream according to parameters in chords_background, pushes the process to the background as a subprocess, and writes data to a file ("chords_data.txt")

## chords_parse.py

Second step of the process. This script reads data from "chords_data.txt" parses it, builds the necessary url for CHORDS upload, and sends the data

## chords_background.py

Reads the parameters set and builds the necessary command for access to UNAVCO stream

## nclient_beta.py

UNAVCO Ntripclient that is used to stream data from UNAVCO's real-time database

You will also need:
Parameter file: "parameter_file.txt" to stream multiple sites at once

# Running the scripts
To run the scripts follow the directions below:

1. Check what python directory you are using and change the #!/bin in Line 1 for each file appropriately. 
This directory needs to be current enough to run the module "psutil"
*If you do not have psutil it can be downloaded through pip or your equivilent method

2. Make sure that all scripts and files are in the same directory

3. Edit the parameter file to input your UNAVCO username and password*
If you do not have one, please reach out to UNAVCO real-time data services and request one

4. Edit the parameter file to add the sites you want data from and the CHORDS portal ID's

5. Run either "./chords_stream.py" or to run in the background "./chords_stream.py &"
This script will run the others in the correct order

6. A file called chords_temp_data will be generated after starting, but it will be empty

7. Check your chords portal to see if the stream is successful

8. This script, if not run from the background, will have to be stopped to run another command in the same terminal window 

# TESTERS ONLY

**Above is the final workflow and how the script is supposed to work. Currently the parameters are as follows for testing**

No need to have parameter file. (These are hardcoded in the chords_background.py file)
This will lead to stream site AC20_RTX and upload it to OLOJ for TZVOLCANO

