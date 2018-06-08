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

def CreateLibrary(csc):
	# Create/Open test suite file.
	print("Creating " + csc + "_SAL.py")
	try:
		os.chdir("robotframework_" + csc + "/Library") 
	except FileNotFoundError:
		os.makedirs("robotframework_" + csc + "/Library", exist_ok=False)
		os.chdir("robotframework_" + csc + "/Library") 
	finally:
		f = open(csc + "_SAL.py","w")

	# Create the import header.
	f.write("import sys\n")
	f.write("import time\n")
	f.write("from SALPY_" + csc + " import *\n")
	f.write("\n")

	# Create the class.
	f.write("class " + csc + "_SAL:\n")
	f.write("\tROBOT_LIBRARY_SCOPE = 'GLOBAL'\n")
	f.write("\n")

	# Create init function.
	f.write("\tdef __init__(self):\n")
	f.write("\t\tself._SAL = SAL_" + csc + "()\n")
	f.write("\t\tself._SAL.setDebugLevel(0)\n")
	f.write("\t\t## SAL " + csc.title() + " Events\n")
	f.write("\t\tself._SAL.salEvent(\"" + csc + "_logevent_SummaryState\")\n")
	f.write("\t\tself._SAL.salEvent(\"" + csc + "_logevent_DetailedState\")\n")
	f.write("\t\tself._SAL.salEvent(\"" + csc + "_logevent_SettingsApplied\")\n")
	f.write("\t\t## SAL " + csc.title() + " Commands\n")
	f.write("\t\tself._SAL.salCommand(\"" + csc + "_command_Start\")\n")
	f.write("\t\tself._SAL.salCommand(\"" + csc + "_command_Standby\")\n")
	f.write("\t\tself._SAL.salCommand(\"" + csc + "_command_Enable\")\n")
	f.write("\t\tself._SAL.salCommand(\"" + csc + "_command_Disable\")\n")
	f.write("\t\t## SAL " + csc.title() + " Telemetry\n")
	f.write("\n")
	f.write("\tdef _afterCommand(self):\n")
	f.write("\t\ttime.sleep(1)\n")
	f.write("\n")
	f.write("\tdef getCurrentTime(self):\n")
	f.write("\t\tdata = self._SAL.getCurrentTime()\n")
	f.write("\t\treturn data\n")
	f.write("\n")

	# Create commands functions
	f.write("\t######## " + csc + " Commands ########\n")
	f.write("\n")
	f.write("\tdef issueStartCommand(self):\n")
	f.write("\t\tdata = " + csc + "_command_StartC()\n")
	f.write("\t\tdata.Start = True\n")
	f.write("\t\tdata.SettingsToApply = \"Default\"\n")
	f.write("\t\tcmdId = self._SAL.issueCommand_Start(data)\n")
	f.write("\t\tself._SAL.waitForCompletion_Start(cmdId, 10)\n")
	f.write("\t\tself._afterCommand()\n")
	f.write("\n")
	f.write("\tdef issueEnableCommand(self):\n")
	f.write("\t\tdata = " + csc + "_command_EnableC()\n")
	f.write("\t\tdata.Enable = True\n")
	f.write("\t\tcmdId = self._SAL.issueCommand_Enable(data)\n")
	f.write("\t\tself._SAL.waitForCompletion_Enable(cmdId, 10)\n")
	f.write("\t\tself._afterCommand()\n")
	f.write("\n")
	f.write("\tdef issueDisableCommand(self):\n")
	f.write("\t\tdata = " + csc + "_command_DisableC()\n")
	f.write("\t\tdata.Disable = True\n")
	f.write("\t\tcmdId = self._SAL.issueCommand_Disable(data)\n")
	f.write("\t\tself._SAL.waitForCompletion_Disable(cmdId, 10)\n")
	f.write("\t\tself._afterCommand()\n")
	f.write("\n")
	f.write("\tdef issueStandbyCommand(self):\n")
	f.write("\t\tdata = " + csc + "_command_StandbyC()\n")
	f.write("\t\tdata.Standby = True\n")
	f.write("\t\tcmdId = self._SAL.issueCommand_Standby(data)\n")
	f.write("\t\tself._SAL.waitForCompletion_Standby(cmdId, 10)\n")
	f.write("\t\tself._afterCommand()\n")
	f.write("\n")
	f.write("\t######## " + csc + " Events ########\n")
	f.write("\n")
	f.write("\tdef getEventSummaryState(self):\n")
	f.write("\t\tdata = " + csc + "_logevent_SummaryStateC()\n")
	f.write("\t\tretVal = self._SAL.getEvent_SummaryState(data)\n")
	f.write("\t\treturn retVal==0, data\n")
	f.write("\n")
	f.write("\tdef getEventDetailedState(self):\n")
	f.write("\t\tdata = " + csc + "_logevent_DetailedStateC()\n")
	f.write("\t\tretVal = self._SAL.getEvent_DetailedState(data)\n")
	f.write("\t\treturn retVal==0, data\n")
	f.write("\n")
	f.write("\tdef getEventSettingsApplied(self):\n")
	f.write("\t\tdata = " + csc + "_logevent_SettingsAppliedC()\n")
	f.write("\t\tretVal = self._SAL.getEvent_SettingsApplied(data)\n")
	f.write("\t\treturn retVal==0, data.Settings\n")
	f.write("\n")

	# Create Utility functions
	f.write("\t######## Utility Functions ########\n")
	f.write("\n")
	f.write("\tdef waitForNextSummaryState(self, wait=300):\n")
	f.write("\t\ttimeout = time.time() + float(wait)\n")
	f.write("\t\tdata = " + csc + "_logevent_SummaryStateC()\n")
	f.write("\t\tretVal = self._SAL.getEvent_SummaryState(data)\n")
	f.write("\t\twhile retVal != 0 and timeout > time.time():\n")
	f.write("\t\t\ttime.sleep(1)\n")
	f.write("\t\t\tretVal = self._SAL.getEvent_SummaryState(data)\n")
	f.write("\t\treturn retVal==0, data.SummaryState\n")
	f.write("\n")
	f.write("\tdef waitForNextDetailedState(self, wait=300):\n")
	f.write("\t\ttimeout = time.time() + float(wait)\n")
	f.write("\t\tdata = " + csc + "_logevent_DetailedStateC()\n")
	f.write("\t\tretVal = self._SAL.getEvent_DetailedState(data)\n")
	f.write("\t\twhile retVal != 0 and timeout > time.time():\n")
	f.write("\t\t\ttime.sleep(1)\n")
	f.write("\t\t\tretVal = self._SAL.getEvent_DetailedState(data)\n")
	f.write("\t\treturn retVal==0, data.DetailedState\n")
	f.write("\n")
	# Create the shutdown utility\n")
	f.write("\tdef __del__(self):\n")
	f.write("\t\tself._SAL.salShutdown()\n")
	f.write("\n")

	# Return to calling directory.
	os.chdir("../../")

if __name__ == '__main__':
	# Get the arguments.
	args = DefineArguments()

	CreateLibrary(args.csc)
