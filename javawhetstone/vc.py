import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

parent_dir = os.path.realpath(os.path.dirname(__file__))
f_output_result="%s/../common/output-test-result.sh" % parent_dir

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)

vc.dump()
btn_run = vc.findViewByIdOrRaise("com.roywhet:id/startButton")
btn_run.touch()
time.sleep(2)

finished = False
key_unit_hash = {
                    "N1": "MFLOPS",
                    "N2": "MFLOPS",
                    "N3": "MOPS",
                    "N4": "MOPS",
                    "N5": "MOPS",
                    "N6": "MFLOPS",
                    "N7": "MOPS",
                    "N8": "MOPS",
                    "MWIPS": "MFLOPS"
                }
while(not finished):
    try:
        time.sleep(30)
        vc.dump()
        results = vc.findViewByIdOrRaise("com.roywhet:id/displayDetails")
        if re.search('Total Elapsed Time', results.getText()):
            finished = True
            print "benchmark finished"
            for line in results.getText().split('\n'):
                line = str(line.strip())
                elements = re.split(r'\s+', line)
                if line.startswith('MWIPS'):
                    units = key_unit_hash['MWIPS']
                    key = "MWIPS"
                    value = elements[1]
                elif line.startswith('N'):
                    units = key_unit_hash[elements[0]]
                    key = "%s_%s" % (elements[0], elements[1])
                    value = elements[2]
                else:
                    continue
                call([f_output_result, key, 'pass', value, units])
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass
