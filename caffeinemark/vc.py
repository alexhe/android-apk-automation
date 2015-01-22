import re
import sys
import os
import time
from subprocess import call

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

# Result collection for LAVA
debug_switcher = False
default_unit = 'points'
result = 'pass'
def collect_score(score_name, result, score, default_unit):
    if debug_switcher == False:
        call(['lava-test-case', score_name, '--result', result, '--measurement', score, '--unit', default_unit])
    else:
        print ['lava-test-case', score_name, '--result', result, '--measurement', score, '--unit', default_unit]

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
vc = ViewClient(device, serialno, **kwargs2)

time.sleep(2)
vc.dump(window='-1')
start_button = vc.findViewByIdOrRaise("com.flexycore.caffeinemark:id/startButton")
start_button.touch()

finished = False
while (not finished):
    time.sleep(1)
    try:
        vc.dump(window='-1')
        vc.findViewByIdOrRaise("com.flexycore.caffeinemark:id/testResultsCellOneTitle")
        finished = True
    except ViewNotFoundException:
        pass
    except RuntimeError as e:
        print e
print "benchmark finished"

total_score = vc.findViewByIdOrRaise("com.flexycore.caffeinemark:id/testResultEntryOverAllScore").getText()
collect_score("Caffeinemark-score", result, total_score, default_unit)

details_button = vc.findViewByIdOrRaise("com.flexycore.caffeinemark:id/testResultsDetailsButton")
details_button.touch()

time.sleep(2)
vc.dump(window='-1')

sieve_name = vc.findViewByIdOrRaise("id/no_id/9").getText()
sieve_score = vc.findViewByIdOrRaise("id/no_id/10").getText()
collect_score("Caffeinemark-Sieve-score", result, sieve_score, default_unit)

loop_name = vc.findViewByIdOrRaise("id/no_id/13").getText()
loop_score = vc.findViewByIdOrRaise("id/no_id/14").getText()
collect_score("Caffeinemark-Loop-score", result, loop_score, default_unit)

logic_name = vc.findViewByIdOrRaise("id/no_id/17").getText()
logic_score = vc.findViewByIdOrRaise("id/no_id/18").getText()
collect_score("Caffeinemark-Collect-score", result, logic_score, default_unit)

string_name = vc.findViewByIdOrRaise("id/no_id/21").getText()
string_score = vc.findViewByIdOrRaise("id/no_id/22").getText()
collect_score("Caffeinemark-String-score", result, string_score, default_unit)

float_name = vc.findViewByIdOrRaise("id/no_id/25").getText()
float_score = vc.findViewByIdOrRaise("id/no_id/26").getText()
collect_score("Caffeinemark-Float-score", result, float_score, default_unit)

method_name = vc.findViewByIdOrRaise("id/no_id/29").getText()
method_score = vc.findViewByIdOrRaise("id/no_id/30").getText()
collect_score("Caffeinemark-Method-score", result, method_score, default_unit)
