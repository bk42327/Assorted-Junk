#!/usr/bin/python3
##
# Fix apfsd assertion for Mac power management under Catalina
# (C) 2020-01-29 Bernd Kunze
#
import subprocess
import os
import time
import sys
import platform


#
# ID
#
__author__ = "Bernd Kunze"
__author_email__ = "bkunze@gmx.net"
__copyright__ = "Copyright (c) 2020"
__license__ = "BSD"
__version__ = "1.03"

#

def main ():
    OS = platform.system ()
    print (sys.argv [0] + " " + __version__)
#
# We only support MacOS
#
    if (OS != "Darwin"):
        print ("Only MacOS supported.")
        exit (0)
    if "10.15" not in str(platform.mac_ver()):
        print ("Script supports only MacOS Catalina (10.15.x)")
        exit (0)

    print ("Waiting for assertion")
    Done = 0;
    Eternity=20
#
# Logic: Run pmset command and analyze output
# If UserEventAgent is present execute kill command twice with a sleep of 5
# seconds, then exit.
# If UserEventAgent is not matched, sleep 60 seconds and retry. Countdown
# Eternity to avoid running forever: If no match after 20 minutes ve nice
# and exit gracefully
#
    while  Done == 0:
        time.sleep (60);
        Result = subprocess.Popen(['pmset', '-g', 'assertions'],
                   stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT)
        PMSet = Result.communicate();
        if "wbc_drain" in str (PMSet):
            os.system ("ps -ef | grep UserEventAgent | grep -v grep | awk '{print $2}'| xargs kill -9");
            time.sleep (5);
            os.system ("ps -ef | grep UserEventAgent | grep -v grep | awk '{print $2}'| xargs kill -9");
            print('\a');
            print('\a');
            Done = 1;
        print ("No match, retrying after 60 seconds");
        Eternity = Eternity-1;
        if Eternity == 0:
            exit (0)
###############################################################################

if __name__ == "__main__":
    main ()
