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
    try:
        found_score_view = False
        while not found_score_view:
            score_view = vc.findViewWithText(content_desc)
            if not score_view:
                device.press('DPAD_DOWN')
                time.sleep(2)
                try:
                    vc.dump()
                except RuntimeError as e:
                    pass
                except ValueError as e:
                    pass
            else:
                found_score_view = True

        score_uid = score_view.getUniqueId()
        uid = int(re.search("id/no_id/(?P<uid>\d+)", score_uid).group('uid'))
        score = vc.findViewByIdOrRaise("id/no_id/%s" % (uid + offset))
        score_text = score.getText()
        if score_text.find("%") > 0:
            score_value, units = score_text.split(" ")
            call([f_output_result, "cfbench_" + content_desc.replace(" ", "_"), 'pass', score_value, units])

        else:
            call([f_output_result, "cfbench_" + content_desc.replace(" ", "_"), 'pass', score_text, default_unit])
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
        time.sleep(5)
        vc.dump()
        progress_button = vc.findViewByIdOrRaise("eu.chainfire.cfbench:id/admob_preference_layout")
        finished = True
    except ViewNotFoundException:
        pass
    except RuntimeError as e:
        pass
    except ValueError as e:
        pass
print("Benchmark Finished")

vc.dump()
result_label = vc.findViewWithTextOrRaise(u'Results')
result_label.touch()
device.press('DPAD_DOWN')
time.sleep(2)

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
get_score_with_content_desc(vc, "Java Efficiency MIPS")
get_score_with_content_desc(vc, "Java Efficiency MSFLOPS")
get_score_with_content_desc(vc, "Java Efficiency MDFLOPS")
get_score_with_content_desc(vc, "Java Efficiency Memory Read")
get_score_with_content_desc(vc, "Java Efficiency Memory Write")
get_score_with_content_desc(vc, "Native Score")
get_score_with_content_desc(vc, "Java Score")
get_score_with_content_desc(vc, "Overall Score")
