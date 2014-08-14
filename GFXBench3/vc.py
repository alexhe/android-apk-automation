import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

def get_score_with_content_desc(vc, content_desc, offset=1):
    score_view =  vc.findViewWithText(content_desc)
    score_uid = score_view.getUniqueId()
    uid = int(re.search("id/no_id/(?P<uid>\d+)", score_uid).group('uid'))
    score = vc.findViewByIdOrRaise("id/no_id/%s" % (uid + offset))
    print "Text :", score.getText()

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
vc = ViewClient(device, serialno, **kwargs2)
time.sleep(2)
vc.dump(window='-1')

#Accept License 
btn_license = vc.findViewByIdOrRaise("android:id/button1")
btn_license.touch()
vc.dump(window='-1')

#Accept Active Internet connection
btn_accept = vc.findViewByIdOrRaise("android:id/button1")
btn_accept.touch()
time.sleep(15)
vc.dump(window='-1')

#Accept Data Sync and Download content 
btn_accept_1 = vc.findViewByIdOrRaise("android:id/button1")
btn_accept_1.touch()
vc.dump(window='-1')

#Wait for download to finish
finished = False
while (not finished):
    time.sleep(1)
    try:
        vc.dump(window='-1')
        vc.findViewByIdOrRaise("android:id/content")
    except ViewNotFoundException:
        finished = True
        pass
    except RuntimeError as e:
        print e

#Start benchmark
test = vc.findViewByIdOrRaise("id/no_id/1")
test.touch()

#Wait while benchmark is running
finished = False
while (not finished):
    time.sleep(1)
    try:
        vc.dump(window='-1')
        vc.findViewByIdOrRaise("com.glbenchmark.glbenchmark27:id/cell_result_maincolumn")
    except ViewNotFoundException:
        finished = True
        pass
    except RuntimeError as e:
        print e
print "benchmark finished"

#Fetch Scores
get_score_with_content_desc(vc, "Manhattan", 5)
get_score_with_content_desc(vc, "1080p Manhattan Offscreen", 5)
get_score_with_content_desc(vc, "T-Rex", 5)
get_score_with_content_desc(vc, "1080p T-Rex Offscreen", 5)
get_score_with_content_desc(vc, "ALU", 5)
get_score_with_content_desc(vc, "1080p ALU Offscreen", 5)
get_score_with_content_desc(vc, "Alpha Blending", 5)
get_score_with_content_desc(vc, "1080p Alpha Blending Offscreen", 5)
get_score_with_content_desc(vc, "Driver Overhead", 5)
get_score_with_content_desc(vc, "1080p Driver Overhead Offscreen", 5)
get_score_with_content_desc(vc, "Fill", 5)

#Drag down to get rest of the test score
device.drag((300,1000), (300,300), 500)

get_score_with_content_desc(vc, "Render Quality", 5)
get_score_with_content_desc(vc, "high precision", 5)
