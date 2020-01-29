#
# Fix apfsd assertion for Mac power management under MacOS Catalina
# (C) 2020-01-29 Bernd Kunze
#
import subprocess
import os
import time
import syslog


Done = 0;

syslog.syslog ('FixSleep starting');
while  Done == 0:
    time.sleep (60);
    Result = subprocess.Popen(['pmset', '-g', 'assertions'],
               stdout=subprocess.PIPE,
               stderr=subprocess.STDOUT)
    PMSet = Result.communicate();
    if "com.apple.apfsd.wbc_drain " in str (PMSet):
        syslog.syslog ('FixSleep identified apfsd assertion');
        os.system ("ps -ef | grep UserEventAgent | grep -v grep | awk '{print $2}'| xargs kill -9");
        syslog.syslog ('Fixsleep kill #1');
        time.sleep (5);
        os.system ("ps -ef | grep UserEventAgent | grep -v grep | awk '{print $2}'| xargs kill -9");
        syslog.syslog ('Fixsleep kill #2');
        Done = 1;
