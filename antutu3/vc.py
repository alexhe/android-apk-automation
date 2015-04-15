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
    except ValueError:
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
default_unit = 'Inapplicable'

call(['lava-test-case', '"AnTuTu 3.3.2 CPU Integer Score"', '--result', 'pass', '--measurement', cpu_int_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 3.3.2 CPU Float Score"', '--result', 'pass', '--measurement', cpu_float_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 3.3.2 2D Score"', '--result', 'pass', '--measurement', twod_score.getText().split(" ")[1], '--units', default_unit])
call(['lava-test-case', '"AnTuTu 3.3.2 3D Score"', '--result', 'pass', '--measurement', threed_score.getText().split(" ")[1], '--units', default_unit])
call(['lava-test-case', '"AnTuTu 3.3.2 Mem Score"', '--result', 'pass', '--measurement', mem_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 3.3.2 DB Score"', '--result', 'pass', '--measurement', db_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 3.3.2 SD Write Score"', '--result', 'pass', '--measurement', sd_write_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 3.3.2 SD Read Score"', '--result', 'pass', '--measurement', sd_read_score.getText(), '--units', default_unit])

total_score = int(cpu_int_score.getText().strip()) + int(cpu_float_score.getText().strip()) + int(twod_score.getText().strip().split(" ")[1])
total_score = total_score + int(threed_score.getText().strip().split(" ")[1]) + int(mem_score.getText().strip()) + int(db_score.getText().strip())
total_score = total_score + int(sd_write_score.getText().strip().split(' ').pop()) + int(sd_read_score.getText().strip().split(' ').pop())
call(['lava-test-case', '"AnTuTu 3.3.2 Total Score"', '--result', 'pass', '--measurement', str(total_score), '--units', default_unit])
