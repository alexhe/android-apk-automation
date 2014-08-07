import re
import sys
import os
import time

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
vc = ViewClient(device, serialno, **kwargs2)
vc.dump(window='-1')

time.sleep(5)
try:
    button_cancel = vc.findViewByIdOrRaise("android:id/button2")
    button_cancel.touch()
except ViewNotFoundException:
    pass

vc.dump(window='-1')
time.sleep(2)
button_ok = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/button_ok")
button_ok.touch()

time.sleep(2)
vc.dump(window='-1')
button_test = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/btn_test")
button_test.touch()

time.sleep(2)
vc.dump(window='-1')
button_start_test = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/button_test")
button_start_test.touch()

finished = False
while(not finished):
    time.sleep(1)
    vc.dump(window='-1')
    try:
        vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/scoreTotal")
        finished = True
    except ViewNotFoundException:
        pass
print "benchmark finished"

total_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/scoreTotal")
cpu_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/scoreCPU")
gpu_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/scoreGPU")
mem_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/scoreMem")
io_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/scoreIO")

call(['lava-test-case', '"AnTuTu 2.8.2 Total Score"', '--result pass', '--measurement', total_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 CPU Score"', '--result pass', '--measurement', cpu_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 GPU Score"', '--result pass', '--measurement', gpu_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 Mem Score"', '--result pass', '--measurement', mem_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 I/O Score"', '--result pass', '--measurement', io_score.getText()])
