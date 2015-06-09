import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

parent_dir = os.path.realpath(os.path.dirname(__file__))
f_output_result="%s/../common/output-test-result.sh"  % parent_dir

default_unit = 'points'

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)

def dump_always():
    success = False
    while not success:
        try:
            vc.dump()
            success = True
        except RuntimeError:
            print("Got RuntimeError when call vc.dump()")
            time.sleep(5)
        except ValueError:
            print("Got ValueError when call vc.dump()")
            time.sleep(5)


def output_result(test_name, measurement):
    call([f_output_result, "antutu332_" + test_name, 'pass',  measurement, default_unit])


# release info and upgrade dialog are not presented
# if there is no connection to Internet
try:
    time.sleep(5)
    dump_always()
    button_cancel = vc.findViewByIdOrRaise("android:id/button2")
    button_cancel.touch()
except ViewNotFoundException:
    pass

try:
    time.sleep(2)
    dump_always()
    button_ok = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/button_ok")
    button_ok.touch()
except ViewNotFoundException:
    pass

found_test_btn = False
while not found_test_btn:
    try:
        dump_always()
        button_test = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/btn_test_now")
        button_test.touch()
        found_test_btn = True
    except ViewNotFoundException:
        print("Not find com.antutu.ABenchMark:id/btn_test_now yet, continue")

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
dump_always()
header = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/layoutScoresHeader")
if not vc.findViewById("com.antutu.ABenchMark:id/layoutScores"):
    header.touch()

time.sleep(2)
dump_always()
mem_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_mem")
cpu_int_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_int")
cpu_float_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_float")
twod_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_2d")
threed_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_3d")
db_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_db")
sd_write_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_sdw")
sd_read_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/text_sdr")

output_result("CPU_Integer_Score", cpu_int_score.getText())
output_result("CPU_Float_Score", cpu_float_score.getText())
output_result("2D_Score", twod_score.getText().strip().split(" ")[1])
output_result("3D_Score", threed_score.getText().strip().split(" ")[1])
output_result("Mem_Score", mem_score.getText())
output_result("DB_Score", db_score.getText())
output_result("SD_Write_Score", sd_write_score.getText().strip().split(' ').pop())
output_result("SD_Read_Score", sd_read_score.getText().strip().split(' ').pop())

total_score = int(cpu_int_score.getText().strip()) + int(cpu_float_score.getText().strip()) + int(twod_score.getText().strip().split(" ")[1])
total_score = total_score + int(threed_score.getText().strip().split(" ")[1]) + int(mem_score.getText().strip()) + int(db_score.getText().strip())
total_score = total_score + int(sd_write_score.getText().strip().split(' ').pop()) + int(sd_read_score.getText().strip().split(' ').pop())
output_result("total_score", str(total_score))
