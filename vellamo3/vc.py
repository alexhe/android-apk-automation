#!/usr/bin/env python
# Author:
# Milosz Wasilewski <milosz.wasilewski@linaro.org>
# Botao Sun <botao.sun@linaro.org>

import sys
import time
import json
from subprocess import call
from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

# Result collection for LAVA
debug_switcher = False
default_unit = 'Points'
def collect_result(testcase, result, score, default_unit):
    if debug_switcher == False:
        call(['lava-test-case', testcase, '--result', result, '--measurement', str(score), '--units', default_unit])
    else:
        print ['lava-test-case', testcase, '--result', result, '--measurement', str(score), '--units', default_unit]

def extract_scores(filename):
    # This is one-line file, read it in a whole
    fileopen = open(filename, 'r')
    jsoncontent = json.load(fileopen)
    result_flag = 'benchmark_results'
    chapter_flag = 'chapter_name'

    for item in jsoncontent:
        if result_flag and chapter_flag in item.keys():
            chapter = item[chapter_flag]
            print str(len(item[result_flag])) + ' test result found in category: ' + chapter
            for elem in item[result_flag]:
                if 'failed' in elem.keys() and 'id' in elem.keys() and 'score' in elem.keys():
                    # Pick up the result
                    if False == elem['failed']:
                        result = 'pass'
                    else:
                        result = 'fail'
                    # Pick up the full test name
                    testcase = chapter + '-' + elem['id']
                    # Pick up the test score
                    score = elem['score']
                    # Submit the result to LAVA
                    collect_result(testcase, result, score, default_unit)
                else:
                    print 'Corrupted test result found, please check it manually.'
                    print 'A valid test result must contain id, score and pass/fail status.'
        else:
            print 'Cannot find ' + result_flag + ' or ' + chapter_flag + ' in test result dictionary. Please check it manually.'
    fileopen.close()

def choose_chapter(vc, chapter_name):
    # ToDo: scroll screen if chapter is not found on the first screen
    vc.dump('-1')
    chapter_tab = vc.findViewWithText(chapter_name)
    if chapter_tab is None:
        device.drag((300, 500), (300, 100), 1000, 20, 0)
        vc.dump('-1')
        chapter_tab = vc.findViewWithTextOrRaise(chapter_name)
    enclosing_tab = chapter_tab.getParent().getParent()
    for child in enclosing_tab.children:
        if child.getClass() == "android.widget.FrameLayout":
           for subchild in child.children:
               if subchild.getId() == "com.quicinc.vellamo:id/card_launcher_run_button":
                   subchild.touch()

kwargs1 = {'verbose': True, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}

vc = ViewClient(device, serialno, **kwargs2)
vc.dump('-1')

# Accept Vellamo EULA
btn_setup_1 = vc.findViewByIdOrRaise("android:id/button1")
btn_setup_1.touch()
vc.dump('-1')

# open settings
vc.dump('-1')
btn_settings = vc.findViewByIdOrRaise('com.quicinc.vellamo:id/main_toolbar_wheel')
btn_settings.touch()

# disable animations
vc.dump('-1')
btn_animations = vc.findViewWithTextOrRaise(u'Make Vellamo even more beautiful')
btn_animations.touch()

# back to the home screen
device.press("KEYCODE_BACK")
chapters = ['Browser', 'Multicore', 'Metal']

for chapter in chapters:
    choose_chapter(vc, chapter)

    # Start benchmark
    vc.dump('-1')
    btn_start = vc.findViewByIdOrRaise("com.quicinc.vellamo:id/main_toolbar_operation_button")
    btn_start.touch()

    # Wait while Vellamo is running benchmark
    finished = False
    while (not finished):
        time.sleep(1)
        try:
            vc.dump(window='-1')
            vc.findViewByIdOrRaise("com.quicinc.vellamo:id/main_toolbar_goback_title")
            btn_no = vc.findViewByIdOrRaise("com.quicinc.vellamo:id/button_no")
            btn_no.touch()
            finished = True
        except ViewNotFoundException:
            pass
        except RuntimeError as e:
            print e

    print "Benchmark finished: %s" % chapter
    device.press("KEYCODE_BACK")
    device.press("KEYCODE_BACK")

return_value = call(['./get_result.sh'])
if return_value == 0:
    extract_scores(filename='chapterscores.json')
else:
    print 'Test result file transfer failed!'
    sys.exit(1)
