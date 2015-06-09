# Author: Botao Sun <botao.sun@linaro.org>

import os
import sys
import time
import re
import xml.dom.minidom
from subprocess import call
from com.dtmilano.android.viewclient import ViewClient

curdir = os.path.realpath(os.path.dirname(__file__))
f_output_result="%s/../common/output-test-result.sh"  % curdir


def collect_score(benchmark_name, run_result, score_number, score_unit):
    call([f_output_result, "glbenchmark251_" + benchmark_name, run_result, str(score_number), score_unit])

def getText(node):
    children = node.childNodes
    rc = []
    for node in children:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def logparser(cached_result_file):
    run_result = 'pass'
    dom = xml.dom.minidom.parse(cached_result_file)
    results = dom.getElementsByTagName('test_result')

    for test in results:
        title = getText(test.getElementsByTagName('title')[0])
        test_type = getText(test.getElementsByTagName('type')[0])
        score_number = getText(test.getElementsByTagName('score')[0])
        fps = getText(test.getElementsByTagName('fps')[0])
        score_unit = getText(test.getElementsByTagName('uom')[0])
        benchmark_name = title.replace(" ", "-").replace(":", "") + "-" + test_type.replace(" ", "-").replace(":", "")

        print benchmark_name, run_result, score_number, score_unit
        collect_score(benchmark_name, run_result, score_number, score_unit)
        if fps != "":
            score_number = fps.split(" ")[0]
            score_unit = fps.split(" ")[1]
            print benchmark_name, run_result, score_number, score_unit
            collect_score(benchmark_name, run_result, score_number, score_unit)

cached_result_file = "last_results_2.5.1.xml"
device, serialno = ViewClient.connectToDeviceOrExit()
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)
time.sleep(2)

vc.dump(window='-1')
test_type = vc.findViewWithText("Performance Tests")
test_type.touch()
time.sleep(2)

# By some reason in order to select all test, a back step is required
vc.dump(window='-1')
test_selection = vc.findViewByIdOrRaise("com.glbenchmark.glbenchmark25:id/buttonAll")
device.press('KEYCODE_BACK')
time.sleep(3)

test_type.touch()
time.sleep(2)
test_selection.touch()
print "All selected!"
time.sleep(3)

# Disable crashed test suites
vc.dump(window='-1')
crashed_test_name = "C24Z24MS4"
print "Test suite " + crashed_test_name + " is going to be disabled!"
crashed_test = vc.findViewWithText(crashed_test_name)
if crashed_test != None:
    crashed_test.touch()
    print "Test suite " + crashed_test_name + " has been excluded!"
    time.sleep(2)
else:
    print "Can not find test suite " + crashed_test_name + ", please check the screen!"

# Start selected test suites
start_button = vc.findViewByIdOrRaise("com.glbenchmark.glbenchmark25:id/buttonStart")
start_button.touch()
time.sleep(2)

finished = False
while (not finished):
    time.sleep(120)
    vc.dump(window='-1')
    flag = vc.findViewWithText("Result processing")
    if flag != None:
        print "GLBenchmark Test Finished!"
        finished = True
        # Give up the result upload
        cancel_button = vc.findViewWithText("Cancel")
        if cancel_button != None:
            cancel_button.touch()
            time.sleep(5)
        else:
            print "Can not find cancel button! Please check the pop up window!"
    else:
        print "GLBenchmark Test is still in progress..."

call_return = call(['%s/get_result.sh' % curdir])
logparser(cached_result_file)
