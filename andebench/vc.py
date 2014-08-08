import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
vc = ViewClient(device, serialno, **kwargs2)
vc.dump('-1')
btn_start_on = vc.findViewByIdOrRaise("com.eembc.coremark:id/btn_start_on")
btn_start_on.touch()
time.sleep(3)
vc.dump('-1')
try:
    progress_button = vc.findViewByIdOrRaise("com.eembc.coremark:id/btn_progress2")
except ViewNotFoundException:
    pass

try:
    progress_button = vc.findViewByIdOrRaise("com.eembc.coremark:id/btn_progress1")
except ViewNotFoundException:
    pass

if not progress_button:
    sys.exit(1)
progress_found = True

while(progress_found):
    time.sleep(3)
    vc.dump('-1')
    found1 = True
    found2 = True
    try:
        progress_button = vc.findViewByIdOrRaise("com.eembc.coremark:id/btn_progress1")
    except ViewNotFoundException:
        found1 = False
    try:
        progress_button = vc.findViewByIdOrRaise("com.eembc.coremark:id/btn_progress2")
    except ViewNotFoundException:
        found2 = False

    if not (found1 or found2):
        progress_found = False
print "benchmark finished"

time.sleep(3)
vc.dump('-1')
results = vc.findViewByIdOrRaise("com.eembc.coremark:id/cid")
results_text = results.getText()
#Results in Iterations/sec:
#AndEMark Native: 6335
#AndEMark Java: 377
result_re = re.compile("^(?P<test_case_id>[a-zA-Z\s]+):\s(?P<measurement>\d+)", re.MULTILINE)
search_results = result_re.finditer(results_text)
for result in search_results:
    call(['lava-test-case', result.group('test_case_id'), '--result', 'pass', '--measurement', result.group('measurement'), '--units', 'Iterations/sec'])
