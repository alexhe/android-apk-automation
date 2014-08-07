#!/bin/bash

#need to be defined for different benchmark apks
activity="com.drolez.nbench/.MainActivity"
apk_file_name="com.drolez.nbench-1.apk"
test_method="python vc.py"
apk_package="com.drolez.nbench"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
