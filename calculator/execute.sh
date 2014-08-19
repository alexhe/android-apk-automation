#!/bin/bash

# need to be defined for different benchmark apks
activity="com.android.calculator2/.Calculator"
apk_file_name=""
test_method="python vc.py"
apk_package="com.android.calculator2"

# following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
