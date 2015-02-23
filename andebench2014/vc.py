import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)
vc.dump()

btn_start_on = vc.findViewByIdOrRaise("com.eembc.coremark:id/btn_start_on")
btn_start_on.touch()
finished = False
while(not finished):
    try:
        time.sleep(20)
        vc.dump()
        btn_close = vc.findViewById("com.eembc.coremark:id/btn_close")
        if btn_close:
            btn_close.touch()
            continue

        results = vc.findViewByIdOrRaise("com.eembc.coremark:id/cid")
        if not results.getText().find("Running") > 0:
            finished = True
            print "benchmark finished"
            result_re = re.compile("(?P<test_case_id>[a-zA-Z\s]+):\s(?P<measurement>\d+)", re.MULTILINE)
            search_results = result_re.finditer(results.getText())
            for result in search_results:
                test_case_id = result.group('test_case_id').strip()
                measurement = result.group('measurement').strip()
                print "%s=%s Iterations/sec" % (test_case_id, measurement)
                call(['lava-test-case', test_case_id, '--result', 'pass', '--measurement', measurement, '--units', 'Iterations/sec'])
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass
