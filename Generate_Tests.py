#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import re
import subprocess
import os
import inspect
import argparse
import shutil
import csc
import StateMachine
import Vars
import Library

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

# Get the arguments.
args = DefineArguments()

# Create the directories for the tests.
working_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

try:
	os.makedirs("robotframework_" + args.csc + "/Library", exist_ok=False)
except FileExistsError:
	print("The directory " + working_dir + "/robotframework_" + args.csc + " already exists.  Continuing...")
except:
	print("Unable to create the" + working_dir + "/robotframework_" + args.csc + " directory. Check the permissions on the " + working_dir + " folder.")
else:
	print("Created robotframework_" + args.csc + "/Library")
	
# Copy the variables resource file
print("Copying the GlobalVars.robot file")
shutil.copyfile("Resources/GlobalVars.robot", "robotframework_" + args.csc + "/GlobalVars.robot")

# Copy the common keywords file
print("Copying the common.robot file")
ifile = open("Resources/common.robot", "r")
ofile = open("robotframework_" + args.csc + "/common.robot", "w")
ofile.write(ifile.read().replace("FILLMEIN", str(args.csc)))

# Copy the Robot-Framework installation and usage instructions.
print("Copying the RobotFramework_Install_Setup_Usage_Instructions.txt file")
shutil.copyfile("Resources/RobotFramework_Install_Setup_Usage_Instructions.txt", "robotframework_" + args.csc + "/RobotFramework_Install_Setup_Usage_Instructions.txt")
# Create the local variables file
Vars.CreateLocalVars(args.csc)

# Create the test suite
StateMachine.CreateTestSuite(args.csc)

# Create the Robot-Framework SAL Python Library
Library.CreateLibrary(args.csc)

