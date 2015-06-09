# Author: Botao Sun <botao.sun@linaro.org>

import os
import sys
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

parent_dir = os.path.realpath(os.path.dirname(__file__))
f_output_result="%s/../common/output-test-result.sh"  % parent_dir

def collect_score(benchmark_name, run_result, score_number, score_unit):
    call([f_output_result, benchmark_name, run_result, score_number, score_unit])

benchmark_name = "BenchmarkPi"
kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)

time.sleep(2)
vc.dump(window='-1')
start_button = vc.findViewByIdOrRaise("gr.androiddev.BenchmarkPi:id/Button01")
start_button.touch()

finished = False
while (not finished):
    time.sleep(1)
    try:
        vc.dump(window='-1')
        vc.findViewByIdOrRaise("android:id/message")
        finished = True
    except ViewNotFoundException:
        pass
    except RuntimeError as e:
        print e
print "benchmark finished"

return_text = vc.findViewByIdOrRaise("android:id/message").getText().split(" ")

flagwordA = "calculated"
flagwordB = "Pi"

if flagwordA in return_text and flagwordB in return_text:
    if return_text.index(flagwordB) == return_text.index(flagwordA) + 1:
        print "This is an valid test result"
        score_number = return_text[return_text.index(flagwordA) + 3]
        score_unit = return_text[return_text.index(flagwordA) + 4].split("!")[0]
        print score_number + " " + score_unit
        run_result = "pass"
    else:
        print "Output string changed, parser need to be updated!"
        sys.exit(1)
else:
    print "Can not find keyword which is supposed to show up!"
    sys.exit(1)

# Submit the test result to LAVA
collect_score("benchmarkpi_" + benchmark_name, run_result, score_number, score_unit)

# Exit the app
vc.dump(window='-1')
exit_button = vc.findViewByIdOrRaise("android:id/button2")
exit_button.touch()
