#!/usr/bin/env python
# -*- coding: utf-8 -*-
import glob
import re
import subprocess
import os
import inspect
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

def CreateTestSuite(csc):
	# Create/Open test suite file.
	print("Creating " + csc + "_StateMachine_Tests.robot")
	try:
		os.chdir("robotframework_" + csc)
	except FileNotFoundError:
		os.makedirs("robotframework_" + csc, exist_ok=False)
		os.chdir("robotframework_" + csc)
	finally:
		f = open(csc + "_StateMachine_Tests.robot","w")

	# Create Settings header.
	f.write("*** Settings ***\n")
	f.write("Documentation    " + csc.title() + " State Machine tests.\n")
	f.write("Suite Setup    Log Many    host=${Host}    CSC=${subSystem}    timeout=${timeout}\n")
	f.write("Library    String\n")
	f.write("Resource    " + csc.title() + "_Global_Vars.robot\n")
	f.write("Library    Library/" + csc + "_SAL.py\n")
	f.write("\n")

	# Create Variables table.
	f.write("*** Variables ***\n")
	f.write("${subSystem}    " + csc + "\n")
	f.write("${timeout}    30s\n")
	f.write("\n")

	# Create Test Case table.
	f.write("*** Test Cases ***\n")

	# Create the Start command test case.
	f.write("Start the System\n")
	f.write("\t[Tags]    functional\n")
	f.write("\tComment    Issue " + csc.title() + " Start Command.\n")
	f.write("\t" + csc.title() + " Start Command\n")
	f.write("\tComment    Verify system enters Disabled State.\n")
	f.write("\tVerify " + csc.title() + " Summary State Event    ${SummaryDisabled}\n")
	f.write("\n")

	# Create the Verify Disabled state test case.
	f.write("Verify Detailed State - Standby\n")
	f.write("\t[Tags]    functional\n")
	f.write("\tComment    Verify system enters Disabled Detailed State.\n")
	f.write("\tVerify " + csc.title() + " Detailed State Event    ${DetailedDisabled}\n")
	f.write("\n")

	# Create the Enable command test case.
	f.write("Enable the System\n")
	f.write("\t[Tags]    functional\n")
	f.write("\tComment    Issue " + csc.title() + " Enable Command.\n")
	f.write("\t" + csc.title() + " Enable Command\n")
	f.write("\tComment    Verify system enters Enabled State.\n")
	f.write("\tVerify " + csc.title() + " Summary State Event    ${SummaryEnabled}\n")
	f.write("\n")

	# Create the Verify Enabled state test case.
	f.write("Verfiy Detailed State - Enabled\n")
	f.write("\t[Tags]    functional\n")
	f.write("\tComment    Verify system enters Parked Detailed State.\n")
	f.write("\tVerify " + csc.title() + " Detailed State Event    ${DetailedEnabled}\n")
	f.write("\n")

	# Create the Disable command test case.
	f.write("Disable the System\n")
	f.write("\t[Tags]    functional\n")
	f.write("\tComment    Issue " + csc.title() + " Disable Command.\n")
	f.write("\t" + csc.title() + " Disable Command\n")
	f.write("\tComment    Verify system enters Disabled State.\n")
	f.write("\tVerify " + csc.title() + " Summary State Event    ${SummaryDisabled}\n")
	f.write("\n")

	# Create the Verify Disabled state test case.
	f.write("Verify System Disabled Detailed State\n")
	f.write("\t[Tags]    functional\n")
	f.write("\tComment    Verify system enters Disabled Detailed State.\n")
	f.write("\tVerify " + csc.title() + " Detailed State Event    ${DetailedDisabled}\n")
	f.write("\n")

	# Create the Standby command test case.
	f.write("Standby the System\n")
	f.write("\t[Tags]    functional\n")
	f.write("\tComment    Issue " + csc.title() + " Standby Command.\n")
	f.write("\t" + csc.title() + " Standby Command\n")
	f.write("\tComment    Verify system enters Standby State.\n")
	f.write("\tVerify " + csc.title() + " Summary State Event    ${SummaryStandby}\n")
	f.write("\n")

	# Create the Verify Standby state test case.
	f.write("Verify System Standby Detailed State\n")
	f.write("\t[Tags]    functional\n")
	f.write("\tComment    Verify system enters Standby Detailed State.\n")
	f.write("\tVerify " + csc.title() + " Detailed State Event    ${DetailedStandby}\n")
	f.write("\n")

	# Return to calling directory.
	os.chdir("../")

if __name__ == '__main__':
	# Get the arguments.
	args = DefineArguments()

	CreateTestSuite(args.csc)
