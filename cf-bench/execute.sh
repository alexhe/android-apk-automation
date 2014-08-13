#!/bin/bash

#need to be defined for different benchmark apks
activity="eu.chainfire.cfbench/.MainActivity"
apk_file_name="CF-Bench-Pro-1.3.apk"
test_method="python vc.py"
apk_package="eu.chainfire.cfbench"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"




