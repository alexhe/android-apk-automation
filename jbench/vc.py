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

vc.dump(window=-1, sleep=5)
btn_jbench = vc.findViewByIdOrRaise("it.JBench.bench:id/button1")
btn_jbench.touch()
time.sleep(2)

finished = False
while(not finished):
    try:
        time.sleep(5)
        vc.dump()
        results = vc.findViewByIdOrRaise("it.JBench.bench:id/textViewResult")
        if re.search('^\d+$', results.getText()):
            finished = True
            print "benchmark finished"
            print "%s=%s" % ("JBench", results.getText().strip())
            call(['lava-test-case', "JBench", '--result', 'pass', '--measurement', results.getText().strip(), '--units', 'points'])
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass
