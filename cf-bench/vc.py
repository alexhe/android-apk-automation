import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

def get_score_with_content_desc(vc, content_desc, offset=1):
    score_view = vc.findViewWithText(content_desc)
    score_uid = score_view.getUniqueId()
    uid = int(re.search("id/no_id/(?P<uid>\d+)", score_uid).group('uid'))
    score = vc.findViewByIdOrRaise("id/no_id/%s" % (uid + offset))
    call(['lava-test-case', content_desc, '--result', 'pass', '--measurement', score.getText()])

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
vc = ViewClient(device, serialno, **kwargs2)
time.sleep(2)
vc.dump(window='-1')

#Start test button
start_button = vc.findViewByIdOrRaise("id/no_id/23")
start_button.touch()

#Wait while cf-bench running 
finished = False
while(not finished):
      time.sleep(1)
      vc.dump('-1')
      try:
         progress_button = vc.findViewByIdOrRaise("eu.chainfire.cfbench:id/admob_preference_layout")
         finished = True  
      except ViewNotFoundException:
         pass
print("Benchmark Finished")

device.drag((300,1000), (150,150), 300)
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
get_score_with_content_desc(vc, "Java Efficiency MIPS")
get_score_with_content_desc(vc, "Java Efficiency MSFLOPS")
get_score_with_content_desc(vc, "Java Efficiency MDFLOPS")
get_score_with_content_desc(vc, "Java Efficiency Memory Read")
get_score_with_content_desc(vc, "Java Efficiency Memory Write")
get_score_with_content_desc(vc, "Native Score")
get_score_with_content_desc(vc, "Java Score")
get_score_with_content_desc(vc, "Overall Score")
