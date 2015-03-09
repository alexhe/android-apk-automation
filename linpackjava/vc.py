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
btn_run = vc.findViewByIdOrRaise("com.LinpackJava:id/startButton")
btn_run.touch()
time.sleep(2)

finished = False
while(not finished):
    try:
        time.sleep(5)
        vc.dump()
        results = vc.findViewByIdOrRaise("com.LinpackJava:id/displayDetails")
        res_match = re.search('Speed\s+(?P<measurement>[\d\.]+)\s+MFLOPS', results.getText())
        if res_match:
            finished = True
            print "benchmark finished"
            speed = res_match.group('measurement').strip()
            print "%s=%s MFLOPS" % ("LinpackJavaSpeed", speed)
            call([f_output_result, "LinpackJavaSpeed", 'pass', speed, 'MFLOPS'])
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass
