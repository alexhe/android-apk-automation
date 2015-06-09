import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException


parent_dir = os.path.realpath(os.path.dirname(__file__))
f_output_result="%s/../common/output-test-result.sh"  % parent_dir


default_unit = 'points'
def get_score_with_content_desc(vc, content_desc, offset=1):
    score_view =  vc.findViewWithText(content_desc)
    score_uid = score_view.getUniqueId()
    uid = int(re.search("id/no_id/(?P<uid>\d+)", score_uid).group('uid'))
    score = vc.findViewByIdOrRaise("id/no_id/%s" % (uid + offset))
    call([f_output_result, "GFXBench3_" + content_desc.replace(" ", "_"), 'pass', score.getText(), default_unit])


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


kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)

# Accept License
time.sleep(2)
dump_always()
btn_license = vc.findViewById("android:id/button1")
if btn_license:
    btn_license.touch()

# Accept Active Internet connection
time.sleep(2)
dump_always()
btn_accept = vc.findViewById("android:id/button1")
if btn_accept:
    btn_accept.touch()

server_connected = False
while not server_connected:
    try:
        time.sleep(15)
        dump_always()
        alert_not_connected = vc.findViewWithText(u'GFXBench could not reach our servers. Please come back later.')
        if alert_not_connected:
            btn_retry = vc.findViewWithTextOrRaise(u'Retry')
            btn_retry.touch()
            continue
        text_connecting = vc.findViewWithText(u'Connecting to server.')
        if text_connecting:
            continue
        server_connected = True
    except ViewNotFoundException:
        pass


# Accept Data Sync and Download content
time.sleep(15)
dump_always()
btn_accept_1 = vc.findViewById("android:id/button1")
if btn_accept_1:
    btn_accept_1.touch()

# Wait for download to finish
finished = False
while (not finished):
    try:
        time.sleep(50)
        dump_always()
        vc.findViewByIdOrRaise("android:id/content")
    except ViewNotFoundException:
        finished = True
        pass
    except RuntimeError as e:
        print e

# Start benchmark
test = vc.findViewByIdOrRaise("id/no_id/1")
test.touch()

# Wait while benchmark is running
finished = False
while (not finished):
    try:
        time.sleep(50)
        dump_always()
        vc.findViewByIdOrRaise("com.glbenchmark.glbenchmark27:id/cell_result_maincolumn")
    except ViewNotFoundException:
        finished = True
        npass
    except RuntimeError as e:
        print e
print "benchmark finished"

# Fetch Scores
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

# Drag down to get rest of the test score
device.drag((300,1000), (300,300), 500)

get_score_with_content_desc(vc, "Render Quality", 5)
get_score_with_content_desc(vc, "high precision", 5)
