# Author: Botao Sun <botao.sun@linaro.org>
import sys
import time
import commands
from subprocess import call
from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

package = "com.android.gallery3d"
testcase = "gallery"
target_view = "gl_root_view"

def collect_score(testcase, run_result):
    call(['lava-test-case', testcase, '--result', run_result])

device, serialno = ViewClient.connectToDeviceOrExit()

vc = ViewClient(device, serialno)

try:
    vc.findViewByIdOrRaise(package + ":id/" + target_view)
    run_result = "pass"
    print target_view + " found!"
    print testcase + " Test PASSED!"
    collect_score(testcase, run_result)
    sys.exit(0)
except ViewNotFoundException:
    run_result = "fail"
    print target_view + " can not be found! Fatal!"
    print testcase + " Test FAILED!"
    collect_score(testcase, run_result)
    sys.exit(1)
