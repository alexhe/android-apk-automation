# Author: Botao Sun <botao.sun@linaro.org>  1
import sys
import time
import commands
from subprocess import call
from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

return_word = ""
testcase = "calculator"
positive_counter = 0

def collect_score(testcase, run_result):
    call(['lava-test-case', testcase, '--result', run_result])

device, serialno = ViewClient.connectToDeviceOrExit()
vc = ViewClient(device, serialno)

for i in range(0, 10):
    try:
        return_word = vc.findViewByIdOrRaise("com.android.calculator2:id/digit" + str(i)).getText()
        if return_word != str(i):
            run_result = "fail"
            print "Number " + str(i) + " can not be found in " + testcase
            print testcase + " Test FAILED!"
            collect_score(testcase, run_result)
            sys.exit(1)
        else:
            print "Number " + str(i) + " found!"
            positive_counter = positive_counter + 1
    except ViewNotFoundException:
        run_result = "fail"
        print "View can not be found! Fatal!"
        print testcase + " Test FAILED!"
        collect_score(testcase, run_result)
        sys.exit(1)

if positive_counter != 10:
    print "Test count failed! Please check the screen!"
    run_result = "fail"
    collect_score(testcase, run_result)
else:
    print testcase + " Test PASSED!"
    run_result = "pass"
    collect_score(testcase, run_result)
