#!/bin/bash

# need to be defined for different benchmark apks
activity="com.android.settings/.Settings"
apk_file_name=""
test_method="python vc.py"
apk_package="com.android.settings"

# following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
