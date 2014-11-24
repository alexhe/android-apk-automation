import re
import sys
import os
import time
from subprocess import call
from HTMLParser import HTMLParser

from com.dtmilano.android.viewclient import ViewClient, ViewNotFoundException

def extract_scores(filename):
    list_of_scores = []

    with open(filename,'r') as infile:
        html = infile.read()
        tree = lxml.html.fromstring(html)

        # Get the Total Score
        h2s_with_span_selector = CSSSelector('div h2 span')
        h2s_with_span = h2s_with_span_selector(tree)
        total_score = h2s_with_span[0].text # pick the string within the span inside the h2
        total_score = int(total_score) # convert to integer
        list_of_scores.append(('Total Score', total_score))

        # Get list of DIVs
        div_in_div_selector = CSSSelector('div div') 
        score_divs = div_in_div_selector(tree) # this returns all divs inside the main div (handled above)
        for div in score_divs:
            #print div.xpath('string()')
            # there's another div inside this div, which has the title
            try:
                title = CSSSelector('div div')(div)[0].xpath('string()') # get all text inside that div
                title = title.encode('UTF-8') # Since some bits contain unicode characters, encode it so 'print' doesn't choke 
                all_li = CSSSelector('div ul li')(div) # List out all LIs inside the div->ul
                if all_li: # Ignore if empty
                    score = re.findall("\d+.\d+", all_li[-1].text)[0] # Find the float (decimal(dot)decimal) inside last text in last LI (-1)

                list_of_scores.append((title, score)) # Append to the list of scores
            except IndexError:
                pass # ignore any errors where list index is out of bounds (we don't want those elements)

    return list_of_scores # finally, return the list

kwargs1 = {'verbose': False, 'ignoresecuredevice': False}
device, serialno = ViewClient.connectToDeviceOrExit(**kwargs1)
kwargs2 = {'startviewserver': True, 'forceviewserveruse': False, 'autodump': False, 'ignoreuiautomatorkilled': True}
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

#Discard low battery level dialog
btn_battery_3 = vc.findViewByIdOrRaise("android:id/button3")
btn_battery_3.touch()
vc.dump('-1')
time.sleep(1)

#Discard no network connection
btn_network_3 = vc.findViewByIdOrRaise("android:id/button3")
btn_network_3.touch()
vc.dump('-1')
time.sleep(1)

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
    time.sleep(1)
    try:
        vc.dump(window='-1')
        vc.findViewByIdOrRaise("com.quicinc.vellamo:id/score_view")
        finished = True
    except ViewNotFoundException:
        pass
    except RuntimeError as e:
        print e

print "Benchmark finished"

return_value = call(['./adb_pull.sh'])
if (return_value == 0): 
    scores = extract_scores(filename='latest_result.html')
    for score in scores:
        call(['lava-test-case', score[0], '--result', 'pass', '--measurement', score[1]])  
else:
    sys.exit(1)
