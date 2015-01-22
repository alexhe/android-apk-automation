import re
import sys
import os
import time
from subprocess import call
from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

default_unit = 'points'

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
vc = ViewClient(device, serialno, **kwargs2)

time.sleep(2)
vc.dump(window='-1')
start_button = vc.findViewByIdOrRaise("com.drolez.nbench:id/start")
start_button.touch()

# benchmark runs for 10 minutes
finished = False
while (not finished):
    time.sleep(1)
    vc.dump(window='-1')
    start_button = vc.findViewByIdOrRaise("com.drolez.nbench:id/start")
    if not start_button.getText().startswith("Benchmark running"):
        finished = True

time.sleep(2)
vc.dump(window='-1')
memory_score = vc.findViewByIdOrRaise("com.drolez.nbench:id/TextView01v")
integer_score = vc.findViewByIdOrRaise("com.drolez.nbench:id/TextView02v")
floating_score = vc.findViewByIdOrRaise("com.drolez.nbench:id/TextView03v")
results = vc.findViewByIdOrRaise("com.drolez.nbench:id/editor")

call(['lava-test-case', 'Nbench memory score', '--result', 'pass', '--measurement', memory_score.getText(), '--units', default_unit])
call(['lava-test-case', 'Nbench integer score', '--result', 'pass', '--measurement', integer_score.getText(), '--units', default_unit])
call(['lava-test-case', 'Nbench floating point score', '--result', 'pass', '--measurement', floating_score.getText(), '--units', default_unit])

test_ids = ['NUMERIC SORT',
            'STRING SORT',
            'BITFIELD',
            'FP EMULATION',
            'FOURIER',
            'ASSIGNMENT',
            'IDEA',
            'HUFFMAN',
            'NEURAL NET',
            'LU DECOMPOSITION']

results_re = re.compile("^(?P<test_case_id>[A-Z\s]+)\s+:\s+(?P<measurement>[\d\.e\+]+)", re.MULTILINE)
for result in results_re.finditer(results.getText()):
    if result.group('test_case_id').strip() in test_ids:
        call(['lava-test-case', result.group('test_case_id').strip(), '--result', 'pass', '--measurement', result.group('measurement'), '--units', 'Iterations/sec'])
