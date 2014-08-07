#!/bin/bash

#need to be defined for different benchmark apks
activity="com.greenecomputing.linpack/.Linpack"
apk_file_name="com.greenecomputing.linpack-1.apk"
test_method="python vc.py"
apk_package="com.greenecomputing.linpack"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
