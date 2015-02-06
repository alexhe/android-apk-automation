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

time.sleep(2)
vc.dump(window='-1')
start_single_button = vc.findViewByIdOrRaise("com.greenecomputing.linpack:id/btnsingle")
start_single_button.touch()
time.sleep(2)
vc.dump(window='-1')
start_single_button = vc.findViewById("com.greenecomputing.linpack:id/btnsingle")
while not start_single_button:
    time.sleep(2)
    vc.dump(window='-1')
    start_single_button = vc.findViewById("com.greenecomputing.linpack:id/btnsingle")

mflops_single_score = vc.findViewByIdOrRaise("com.greenecomputing.linpack:id/txtmflops_result")
time_single_score = vc.findViewByIdOrRaise("com.greenecomputing.linpack:id/txttime_result")

call(['lava-test-case', '"Linpack MFLOPS Single Score"', '--result', 'pass', '--measurement', mflops_single_score.getText(), '--units', 'MFLOPS'])
call(['lava-test-case', '"Linpack Time Single Score"', '--result', 'pass', '--measurement', time_single_score.getText(), '--units', 'seconds'])

start_multi_button = vc.findViewByIdOrRaise("com.greenecomputing.linpack:id/btncalculate")
start_multi_button.touch()
time.sleep(2)
vc.dump(window='-1')
start_single_button = vc.findViewById("com.greenecomputing.linpack:id/btnsingle")
while not start_single_button:
    time.sleep(2)
    vc.dump(window='-1')
    start_single_button = vc.findViewById("com.greenecomputing.linpack:id/btnsingle")

mflops_multi_score = vc.findViewByIdOrRaise("com.greenecomputing.linpack:id/txtmflops_result")
time_multi_score = vc.findViewByIdOrRaise("com.greenecomputing.linpack:id/txttime_result")

call(['lava-test-case', '"Linpack MFLOPS Multi Score"', '--result', 'pass', '--measurement', mflops_multi_score.getText(), '--units', 'MFLOPS'])
call(['lava-test-case', '"Linpack Time Multi Score"', '--result', 'pass', '--measurement', time_multi_score.getText(), '--units', 'seconds'])
