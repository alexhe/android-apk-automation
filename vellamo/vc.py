import re
import sys
import os
import time
from subprocess import call
from HTMLParser import HTMLParser
from xml.etree import ElementTree

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

parent_dir = os.path.realpath(os.path.dirname(__file__))


class AllEntities:
    def __getitem__(self, key):
        #key is your entity, you can do whatever you want with it here
        return ""

default_unit = 'points'
def extract_scores(filename):

    testf = open(filename, 'r')

    parser = ElementTree.XMLParser()
    parser.parser.UseForeignDTD(True)
    parser.entity = AllEntities()

    tree = ElementTree.parse(testf, parser=parser)

    # search for h2 header
    totalscore = -1
    for node in tree.iter('h2'):
        if node.text.startswith("Total Score"):
            totalscore = node.getchildren()[0].text

    benchmarks = []
    for node in tree.iter('div'):
        isscorenode = False
        if node.find("./img") is not None:
            isscorenode = True
        if isscorenode:
            scorename = node.find("./div").text.strip()
            benchmark_dict = {'name': scorename, 'values': {}}

            for subscore in node.findall(".//li"):
                 key, value = subscore.text.split(":")
                 benchmark_dict['values'].update({key: value.strip()})
            benchmarks.append(benchmark_dict)

    call(['lava-test-case', "Vellamo 1.0.6", '--result', 'pass', '--measurement', totalscore, '--units', default_unit])
    for benchmark in benchmarks:
        name = benchmark['name']
        result = 'pass'
        if 'failed' in benchmark['values'].keys():
            result = 'fail'
        for subbenchkey, subbenchvalue in benchmark['values'].items():
            if subbenchkey != 'failed':
                call(['lava-test-case', "%s %s" % (name, subbenchkey), '--result', result, '--measurement', subbenchvalue, '--units', default_unit])

kwargs1 = {'verbose': True, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True, 'compresseddump': False}

vc = ViewClient(device, serialno, **kwargs2)
vc.dump('-1')

#Accept Vellamo EULA
btn_setup_1 = vc.findViewByIdOrRaise("android:id/button1")
btn_setup_1.touch()
vc.dump('-1')

#Edit list of websites button
btn_setup_2 = vc.findViewByIdOrRaise("android:id/button2")
btn_setup_2.touch()
vc.dump('-1')
time.sleep(1)

try:
    #Discard low battery level dialog
    btn_battery_3 = vc.findViewByIdOrRaise("android:id/button3")
    btn_battery_3.touch()
    vc.dump('-1')
    time.sleep(1)
except ViewNotFoundException:
    # doesn't show up on all boards
    pass

#Discard no network connection
try:
    btn_network_3 = vc.findViewByIdOrRaise("android:id/button3")
    btn_network_3.touch()
    vc.dump('-1')
    time.sleep(1)
except ViewNotFoundException:
    # doesn't show up on all boards
    pass

#Disable safeguards
btn_more = vc.findViewWithTextOrRaise("More")
btn_more.touch()
vc.dump('-1')
time.sleep(1)

btn_safeguards = vc.findViewWithTextOrRaise("Override Safeguards")
btn_safeguards.touch()
vc.dump('-1')
time.sleep(1)

#Start Button
btn_start_on = vc.findViewWithTextOrRaise("Start")
btn_start_on.touch()
vc.dump('-1')
time.sleep(5)

#Discard Enable Tutorial dialog
btn_setup_3 = vc.findViewByIdOrRaise("android:id/button2")
btn_setup_3.touch()

#Wait while Vellamo is running benchmark
finished = False
while (not finished):
    time.sleep(30)
    try:
        vc.dump(window='-1')
        vc.findViewByIdOrRaise("com.quicinc.vellamo:id/score_view")
        finished = True
    except ViewNotFoundException:
        pass
    except RuntimeError as e:
        print e
        pass
    except ValueError:
        pass

print "Benchmark finished"

return_value = call(['%s/adb_pull.sh' % parent_dir])
if (return_value == 0):
    extract_scores(filename='latest_result.html')
else:
    sys.exit(1)
