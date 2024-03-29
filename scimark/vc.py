import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

parent_dir = os.path.realpath(os.path.dirname(__file__))
f_output_result="%s/../common/output-test-result.sh"  % parent_dir

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

time.sleep(5)
dump_always()
btn_java_bench = vc.findViewWithTextOrRaise(u'Java bench')
btn_java_bench.touch()

keys = [ "FFT (1024)", "SOR (100x100)", "Monte Carlo", \
         "Sparse matmult (N=1000, nz=5000)", "LU (100x100)", "Composite Score"]
finished = False
while(not finished):
    try:
        time.sleep(60)
        dump_always()
        results = vc.findViewByIdOrRaise("net.danielroggen.scimark:id/textViewResult")
        if results.getText().find("Done") > 0:
            finished = True
            print "benchmark finished"
            for line in results.getText().replace(": \n", ":").split("\n"):
                line = str(line.strip())
                key_val = line.split(":")
                if len(key_val) == 2:
                    if key_val[0].strip() in keys:
                        key = key_val[0].strip().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
                        call([f_output_result, "scimark_" + key, 'pass', key_val[1].strip(), 'Mflops'])
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass
