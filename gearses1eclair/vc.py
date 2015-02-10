# Author: Botao Sun <botao.sun@linaro.org>

import os
import sys
import time
from subprocess import call

parent_dir = os.path.realpath(os.path.dirname(__file__))

def collect_score(benchmark_name, run_result, score_number, score_unit):
    call(['lava-test-case', benchmark_name, '--result', run_result, '--measurement', str(score_number), '--units', score_unit])

benchmark_name = "GearsES1eclair"
time.sleep(60)

call_return = call(['%s/get_raw_logcat.sh' % parent_dir])
if call_return != 0:
    print "Capture real time logcat output failed!"
    sys.exit(1)

raw_output_file = "logcat_gearses1eclair.txt"
flagwordA = "a3d_GLES_dump"
flagwordB = "fps"
result_collector = []

logfile = open(raw_output_file, "r")
for line in logfile:
    linelist = line.strip("\n").strip("\r").split(" ")
    linelist = filter(None, linelist)
    for itemA in linelist:
        if itemA.find(flagwordA) != -1:
            for itemB in linelist:
                if itemB.find(flagwordB) != -1:
                    print linelist
                    for i in range(0, len(linelist)):
                        grouplist = linelist[i].split("=")
                        if len(grouplist) == 2 and grouplist[0] == flagwordB:
                            result_collector.append(grouplist[1])
logfile.close()

print result_collector
if len(result_collector) > 0:
    average_fps = sum(float(element) for element in result_collector) / len(result_collector)
    score_number = average_fps
    run_result = "pass"
    score_unit = flagwordB
    print "The average FPS in this test run is " + str(score_number)
else:
    print "The collector is empty, no actual result received!"
    sys.exit(1)

# Submit the test result to LAVA
collect_score(benchmark_name, run_result, score_number, score_unit)
