import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

default_unit = 'points'
def get_score_with_text(vc, text, offset=1):
    score_view = vc.findViewWithTextOrRaise(text)
    score_uid = score_view.getUniqueId()
    uid = int(re.search("id/no_id/(?P<uid>\d+)", score_uid).group('uid'))
    score = vc.findViewByIdOrRaise("id/no_id/%s" % (uid + offset))
    call(['lava-test-case', text.strip(), '--result', 'pass', '--measurement', score.getText().strip(), '--units', default_unit])

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)
while True:
    try:
        time.sleep(5)
        vc.dump('-1')
        btn_start = vc.findViewWithTextOrRaise("Run SmartBench")
        btn_start.touch()
        break
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass

finished = False
while not finished:
    try:
        time.sleep(5)
        vc.dump('-1')
        btn_results = vc.findViewWithTextOrRaise("Display Index Scores")
        btn_results.touch()
        time.sleep(3)
        print "benchmark finished"
        finished = True
    except ViewNotFoundException:
        pass
    except RuntimeError:
        pass
    except ValueError:
        pass
