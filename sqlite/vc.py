import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

def get_score_with_text(vc, text, offset=1):
    score_view = vc.findViewWithTextOrRaise(text)
    score_uid = score_view.getUniqueId()
    uid = int(re.search("id/no_id/(?P<uid>\d+)", score_uid).group('uid'))
    score = vc.findViewByIdOrRaise("id/no_id/%s" % (uid + offset))
    call(['lava-test-case', text.strip(), '--result', 'pass', '--measurement', score.getText().strip()])

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
vc = ViewClient(device, serialno, **kwargs2)
vc.dump('-1')
btn_start = vc.findViewByIdOrRaise("com.wtsang02.sqliteutil.activities:id/btStart")
btn_start.touch()

finished = False
btn_results = None
while(not finished):
    try:
        time.sleep(5)
        vc.dump('-1')
        btn_results = vc.findViewById("com.wtsang02.sqliteutil.activities:id/btToResults")
        if btn_results:
            finished = True
    except RuntimeError:
        pass
print "benchmark finished"
btn_results.touch()

time.sleep(1)
vc.dump('-1')
get_score_with_text(vc, "Insert 200 Statments ")
get_score_with_text(vc, "Insert 15000 Statments in Transaction ")
get_score_with_text(vc, "Update 500 Statments ")
get_score_with_text(vc, "Update 15000 Statments in Transaction ")
get_score_with_text(vc, "Select 15000 Statements ")
get_score_with_text(vc, "Delete 200 Statments ")
get_score_with_text(vc, "Delete 15000 Statments in Transaction ")
get_score_with_text(vc, "Overall Avg QPS ")

