# Author: Botao Sun <botao.sun@linaro.org>
import sys
import time
import commands
from subprocess import call
from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

keyword = "Google"
return_word = ""
testcase = "WebKit-Browser"

def collect_score(testcase, run_result):
    call(['lava-test-case', testcase, '--result', run_result])

device, serialno = ViewClient.connectToDeviceOrExit()

vc = ViewClient(device, serialno)

try:
    return_word = vc.findViewByIdOrRaise("com.android.browser:id/title").getText()
except ViewNotFoundException:
    run_result = "fail"
    print "View can not be found! Fatal!"
    print testcase + " Test FAILED!"
    collect_score(testcase, run_result)
    sys.exit(1)

if return_word == keyword:
    run_result = "pass"
    print testcase + " Test PASSED!"
    collect_score(testcase, run_result)
else:
    print "Check point text doesn't match!"
    run_result = "fail"
    print testcase + " Test FAILED!"
    collect_score(testcase, run_result)
