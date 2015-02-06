import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

default_unit = 'points'
def get_score_with_content_desc(vc, content_desc, offset=1):
    try:
        score_view = vc.findViewWithTextOrRaise(content_desc)
        score_uid = score_view.getUniqueId()
        uid = int(re.search("id/no_id/(?P<uid>\d+)", score_uid).group('uid'))
        score = vc.findViewByIdOrRaise("id/no_id/%s" % (uid + offset))
        score_text = score.getText()
        if score_text.find("%") > 0:
            score_value, units = score_text.split(" ")
            call(['lava-test-case', content_desc, '--result', 'pass', '--measurement', score_value, '--units', units])
        else:
            call(['lava-test-case', content_desc, '--result', 'pass', '--measurement', score_text, '--units', default_unit])
    except ViewNotFoundException:
        print "%s not found" % (content_desc)
        pass

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}
vc = ViewClient(device, serialno, **kwargs2)
time.sleep(2)
vc.dump(window='-1')

#Start test button
start_button = vc.findViewWithTextOrRaise("Full Benchmark")
start_button.touch()

#Wait while cf-bench running
finished = False
while(not finished):
    try:
        time.sleep(1)
        vc.dump('-1')
        progress_button = vc.findViewByIdOrRaise("eu.chainfire.cfbench:id/admob_preference_layout")
        finished = True
    except ViewNotFoundException:
        pass
    except RuntimeError as e:
        print e
print("Benchmark Finished")

device.drag((300,1000), (300,300), 300)
time.sleep(5)
vc.dump(window='-1')

#Fetch Scores
get_score_with_content_desc(vc, "Native MIPS")
get_score_with_content_desc(vc, "Java MIPS")
get_score_with_content_desc(vc, "Native MSFLOPS")
get_score_with_content_desc(vc, "Java MSFLOPS")
get_score_with_content_desc(vc, "Native MDFLOPS")
get_score_with_content_desc(vc, "Java MDFLOPS")
get_score_with_content_desc(vc, "Native MALLOCS")
get_score_with_content_desc(vc, "Native Memory Read")
get_score_with_content_desc(vc, "Java Memory Read")
get_score_with_content_desc(vc, "Native Memory Write")
get_score_with_content_desc(vc, "Java Memory Write")
get_score_with_content_desc(vc, "Native Disk Read")
get_score_with_content_desc(vc, "Native Disk Write")

# drag screen once more to reveal remaining results
device.drag((300,1000), (300,300), 300)
time.sleep(5)
vc.dump(window='-1')

get_score_with_content_desc(vc, "Java Efficiency MIPS")
get_score_with_content_desc(vc, "Java Efficiency MSFLOPS")
get_score_with_content_desc(vc, "Java Efficiency MDFLOPS")
get_score_with_content_desc(vc, "Java Efficiency Memory Read")
get_score_with_content_desc(vc, "Java Efficiency Memory Write")
get_score_with_content_desc(vc, "Native Score")
get_score_with_content_desc(vc, "Java Score")
get_score_with_content_desc(vc, "Overall Score")
