import re
import sys
import os
import time

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

def collect_score(score_name, score_widget):
    #call(['lava-test-case', score_name, '--result pass', '--measurement', score_widget.getText()])
    print ['lava-test-case', score_name, '--result pass', '--measurement', score_widget.getText()]

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
    vc.dump(window='-1')
    try:
        vc.findViewByIdOrRaise("com.flexycore.caffeinemark:id/testResultsCellOneTitle")
        finished = True
    except ViewNotFoundException:
        pass
print "benchmark finished"

total_score = vc.findViewByIdOrRaise("com.flexycore.caffeinemark:id/testResultEntryOverAllScore")
collect_score("Caffeinemark score", total_score)

details_button = vc.findViewByIdOrRaise("com.flexycore.caffeinemark:id/testResultsDetailsButton")
details_button.touch()

time.sleep(2)
vc.dump(window='-1')

sieve_name = vc.findViewByIdOrRaise("id/no_id/9").getText()
sieve_score = vc.findViewByIdOrRaise("id/no_id/10")
collect_score("Caffeinemark Sieve score", sieve_score)

loop_name = vc.findViewByIdOrRaise("id/no_id/13").getText()
loop_score = vc.findViewByIdOrRaise("id/no_id/14")
collect_score("Caffeinemark Loop score", loop_score)

logic_name = vc.findViewByIdOrRaise("id/no_id/17").getText()
logic_score = vc.findViewByIdOrRaise("id/no_id/18")
collect_score("Caffeinemark Collect score", logic_score)

string_name = vc.findViewByIdOrRaise("id/no_id/21").getText()
string_score = vc.findViewByIdOrRaise("id/no_id/22")
collect_score("Caffeinemark String score", string_score)

float_name = vc.findViewByIdOrRaise("id/no_id/25").getText()
float_score = vc.findViewByIdOrRaise("id/no_id/26")
collect_score("Caffeinemark Float score", float_score)

method_name = vc.findViewByIdOrRaise("id/no_id/29").getText()
method_score = vc.findViewByIdOrRaise("id/no_id/30")
collect_score("Caffeinemark Method score", method_score)
