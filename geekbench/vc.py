import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

def get_score_with_content_desc(vc, content_desc, offset=1):
    score_view = vc.findViewWithContentDescriptionOrRaise(content_desc)
    score_uid = score_view.getUniqueId()
    uid = int(re.search("id/no_id/(?P<uid>\d+)", score_uid).group('uid'))
    score = vc.findViewByIdOrRaise("id/no_id/%s" % (uid + offset))
    call(['lava-test-case', content_desc, '--result', 'pass', '--measurement', score.getContentDescription()])

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
vc = ViewClient(device, serialno, **kwargs2)

time.sleep(2)
vc.dump(window='-1')
start_button = vc.findViewByIdOrRaise("ca.primatelabs.geekbench2:id/runBenchmarks")
start_button.touch()

time.sleep(2)
finished = False
while (not finished):
    time.sleep(1)
    try:
        vc.dump(window='-1')
        vc.findViewByIdOrRaise("android:id/progress")
    except ViewNotFoundException:
        finished = True
        pass
    except RuntimeError as e:
        print e
print "benchmark finished"

time.sleep(3)
# need to touch the screen to update the view structure
device.touch(300,300)
time.sleep(1)
device.drag((300,1000), (300,300), 500)
time.sleep(1)
device.drag((1000,300), (300,300), 500)
time.sleep(1)
device.press("KEYCODE_MENU")
time.sleep(1)
device.press("KEYCODE_MENU")
time.sleep(1)
vc.dump(window='-1')
get_score_with_content_desc(vc, "Geekbench Score", 4)
get_score_with_content_desc(vc, "Integer")
get_score_with_content_desc(vc, "Floating Point")
get_score_with_content_desc(vc, "Memory")
get_score_with_content_desc(vc, "Stream")
