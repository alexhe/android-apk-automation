#!/bin/bash

#need to be defined for different benchmark apks
activity="gr.androiddev.BenchmarkPi/.BenchmarkPi"
apk_file_name="gr.androiddev.BenchmarkPi-1.apk"
test_method="python vc.py"
apk_package="gr.androiddev.BenchmarkPi"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
