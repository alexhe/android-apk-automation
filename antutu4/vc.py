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

#Wait while application loads
time.sleep(2)
vc.dump(window='-1')

# Close the update dialog if it exists
try:
    cncl_btn = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/negative_btn")
    cncl_btn.touch()
except ViewNotFoundException:
    pass

#Start test button
vc.dump(window='-1')
start_button = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/test_btn")
start_button.touch()

#Start all test button
vc.dump(window='-1')
start_test_button = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/test_all_btn")
start_test_button.touch()

#Wait while antutu4 is running benchmark
finished = False
while(not finished):
    try:
        time.sleep(1)
        vc.dump('-1')
        progress_button = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/detail_content")
        finished = True
    except ViewNotFoundException:
        pass
    except ValueError:
        print "Problem with UIAutomator"

print("Benchmark Finished")

#Change view to Test tab
vc.dump(window='-1')
start_test_tab_button = vc.findViewByIdOrRaise("id/no_id/16")
start_test_tab_button.touch()
#GEt detail scores
vc.dump(window='-1')
detail_detail_button = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/detail_btn")
detail_detail_button.touch()

#start_button = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/score_text")
#text = start_button.getText()

#Get the score
vc.dump(window='-1')
multitask_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/ue_multitask_text")
dalvik_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/ue_dalvik_text")
cpu_integer_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/cpu_int_text")
cpu_float_point_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/cpu_float_text")
ram_operation_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/mem_text")
ram_speed_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/ram_text")
twod_graphics_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/gpu_2d_text")
threed_graphics_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/gpu_3d_text")
storage_io_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/io_sdw_text")
database_io_score = vc.findViewByIdOrRaise("com.antutu.ABenchMark:id/io_db_text")
default_unit = 'Points'

call(['lava-test-case', '"AnTuTu 4.0.3 UX Multitask Score"', '--result', 'pass', '--measurement', multitask_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 UX Dalvik Score"', '--result', 'pass', '--measurement', dalvik_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 CPU Integer Score"', '--result', 'pass', '--measurement', cpu_integer_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 CPU Float-Point Score"', '--result', 'pass', '--measurement', cpu_float_point_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 RAM Operation Score"', '--result', 'pass', '--measurement', ram_operation_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 RAM Speed Score"', '--result', 'pass', '--measurement', ram_speed_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 GPU 2D Graphics Score"', '--result', 'pass', '--measurement', twod_graphics_score.getText().split(" ")[1], '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 GPU 3D Graphics Score"', '--result', 'pass', '--measurement', threed_graphics_score.getText().split(" ")[1], '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 IO Storage I/O Score"', '--result', 'pass', '--measurement', storage_io_score.getText(), '--units', default_unit])
call(['lava-test-case', '"AnTuTu 4.0.3 IO Database I/O Score"', '--result', 'pass', '--measurement', database_io_score.getText(), '--units', default_unit])

total_score = 0
total_score = total_score + int(multitask_score.getText().strip()) + int(dalvik_score.getText().strip())
total_score = total_score + int(cpu_integer_score.getText().strip()) + int(cpu_float_point_score.getText().strip())
total_score = total_score + int(ram_operation_score.getText().strip()) + int(ram_speed_score.getText().strip())
total_score = total_score + int(twod_graphics_score.getText().strip().split(" ")[1]) + int(threed_graphics_score.getText().strip().split(" ")[1])
total_score = total_score + int(storage_io_score.getText().strip().split(' ').pop()) + int(database_io_score.getText().strip().split(' ').pop())
call(['lava-test-case', '"AnTuTu 4.0.3 Total Score"', '--result', 'pass', '--measurement', str(total_score), '--units', default_unit])
