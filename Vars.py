#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import re
import subprocess
import os
import argparse
import csc

def DefineArguments():
    """Argument parser."""
    parser = argparse.ArgumentParser(
        description='Determine which CSC to generate State Machine tests.')
    parser.add_argument(
        '-c',
        '--csc',
        metavar='CSC',
        dest='csc',
        type = str.lower,
        required=True,
        choices=str(csc.csc_array)[1:-1],
        help='''For which CSC do you want to generate tests? ''')
    args = parser.parse_args()
    return args

def CreateLocalVars(csc):
	# Create/Open GlobalVars file.
	print("Creating " + csc + "_LocalVars.robot")
	try:
		os.chdir("robotframework_" + csc)
	except FileNotFoundError:
		os.makedirs("robotframework_" + csc, exist_ok=False)
		os.chdir("robotframework_" + csc)
	finally:
		f = open(csc + "_LocalVars.txt","w")

	# Create the header.
	f.write("# vi:syntax=cmake\n")
	f.write("#  Arguments file for testing the " + csc + "\n")
	f.write("\n")

	# Define location test reports
	f.write("#  Output directory\n")
	f.write("-d " + os.environ['HOME'] + "/Reports/" + csc + "_RegressionTests\n")
	f.write("\n")

	# Define tests to skip
	f.write("#  Specify tags to NOT run\n")
	f.write("-e skipped\n")
	f.write("#-e TSS*\n")
	f.write("\n")

	# Define non-critical tags
	f.write("# Specify non-critical failures\n")
	f.write("--noncritical TSS*\n")
	f.write("\n")

	# Set dry run mode
	f.write("# Dry run mode\n")
	f.write("#--dryrun\n")
	f.write("\n")

	# User informatin
	f.write("#  Redefine default variables\n")
	f.write("--variable UserName:FILLMEIN\n")
	f.write("--variable PassWord:FILLMEIN\n")
	f.write("--variable OpenspliceVersion:6.7.170523OSS\n")
	f.write("--variable OpenspliceDate:2017-07-31\n")
	f.write("--variable SALVersion:3.7.0\n")
	f.write("\n")

	# Return to calling directory.
	os.chdir("../")

if __name__ == '__main__':
	# Get the arguments.
	args = DefineArguments()

	CreateLocalVars(args.csc)
