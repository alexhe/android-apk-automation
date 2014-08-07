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

time.sleep(2)
vc.dump(window='-1')
start_button = vc.findViewByIdOrRaise("ca.primatelabs.geekbench2:id/runBenchmarks")
start_button.touch()

time.sleep(2)
finished = False
while (not finished):
    time.sleep(1)
    vc.dump(window='-1')
    try:
        vc.findViewByIdOrRaise("android:id/progress")
    except ViewNotFoundException:
        finished = True
        pass
print "benchmark finished"

time.sleep(3)
# need to touch the screen to update the view structure
device.touch(300,300)
time.sleep(1)
device.drag((300,1000), (300,300), 500)
time.sleep(1)
device.drag((1000,300), (300,300), 500)
time.sleep(1)
vc.dump(window='-1')
total_score = vc.findViewByIdOrRaise("id/no_id/15")
integer_score = vc.findViewByIdOrRaise("id/no_id/14")
floating_score = vc.findViewByIdOrRaise("id/no_id/18")
memory_score = vc.findViewByIdOrRaise("id/no_id/21")
stream_score = vc.findViewByIdOrRaise("id/no_id/24")

call(['lava-test-case', '"Geekbench Total Score"', '--result pass', '--measurement', total_score.getContentDescription()])
call(['lava-test-case', '"Geekbench Integer Score"', '--result pass', '--measurement', integer_score.getContentDescription()])
call(['lava-test-case', '"Geekbench Floating Point Score"', '--result pass', '--measurement', floating_score.getContentDescription()])
call(['lava-test-case', '"Geekbench Memory Score"', '--result pass', '--measurement', memory_score.getContentDescription()])
call(['lava-test-case', '"Geekbench Stream Score"', '--result pass', '--measurement', stream_score.getContentDescription()])
