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
time.sleep(5)
vc.dump(window='-1')

# release info and upgrade dialog are not presented
# if there is no connection to Internet
try:
    button_cancel = vc.findViewByIdOrRaise("android:id/button2")
    button_cancel.touch()
except ViewNotFoundException:
    pass

try:
    vc.dump(window='-1')
    time.sleep(2)
    button_ok = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/button_ok")
    button_ok.touch()
except ViewNotFoundException:
    pass

time.sleep(2)
vc.dump(window='-1')
button_test = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/btn_test_now")
button_test.touch()

#time.sleep(2)
#vc.dump(window='-1')
#button_start_test = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/button_test")
#button_start_test.touch()

finished = False
while(not finished):
    time.sleep(1)
    try:
        vc.dump(window='-1')
        if vc.findViewById("com.antutu.ABenchMark:id/layoutScoresHeader"):
            finished = True
    except RuntimeError:
        pass

print "benchmark finished"

# close unnecessary windows if they appear
for index in range(0, 3):
    time.sleep(1)
    vc.dump(window='-1')
    if vc.findViewById("com.antutu.ABenchMark:id/num_1"):
        break
    else:
        device.press('KEYCODE_BACK')

time.sleep(2)
vc.dump(window='-1')
header = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/layoutScoresHeader")
if not vc.findViewById("com.antutu.ABenchMark:id/layoutScores"):
    header.touch()

time.sleep(2)
vc.dump(window='-1')
mem_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_mem")
cpu_int_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_int")
cpu_float_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_float")
twod_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_2d")
threed_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_3d")
db_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_db")
sd_write_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_sdw")
sd_read_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_sdr")

call(['lava-test-case', '"AnTuTu 2.8.2 CPU Integer Score"', '--result', 'pass', '--measurement', cpu_int_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 CPU Float Score"', '--result', 'pass', '--measurement', cpu_float_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 2D Score"', '--result', 'pass', '--measurement', twod_score.getText().split(" ")[1]])
call(['lava-test-case', '"AnTuTu 2.8.2 3D Score"', '--result', 'pass', '--measurement', threed_score.getText().split(" ")[1]])
call(['lava-test-case', '"AnTuTu 2.8.2 Mem Score"', '--result', 'pass', '--measurement', mem_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 DB Score"', '--result', 'pass', '--measurement', db_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 SD Write Score"', '--result', 'pass', '--measurement', sd_write_score.getText()])
call(['lava-test-case', '"AnTuTu 2.8.2 SD Read Score"', '--result', 'pass', '--measurement', sd_write_score.getText()])
