#!/bin/bash

#need to be defined for different benchmark apks
activity="com.eembc.coremark/.tabs"
apk_file_name="com.eembc.coremark-1.apk"
test_method="python vc.py"
apk_package="com.eembc.coremark"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
