#!/bin/bash

#need to be defined for different benchmark apks
activity="com.quicinc.vellamo/.Vellamo"
apk_file_name="com.quicinc.vellamo-1.apk"
test_method="python vc.py"
apk_package="com.quicinc.vellamo"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
timeout=30m
main "$@"




