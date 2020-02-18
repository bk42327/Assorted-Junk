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
__version__ = "1.02"

#
OS = platform.system ()
print (sys.argv [0], __version__)
print (OS)
if (OS != "Darwin"):
    printf ("Only MacOS supported.")
    exit (0)
#
Done = 0;
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
