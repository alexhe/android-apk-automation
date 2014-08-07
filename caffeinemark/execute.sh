#!/bin/bash

#need to be defined for different benchmark apks
activity="com.flexycore.caffeinemark/.Application"
apk_file_name="com.flexycore.caffeinemark-1.apk"
test_method="python vc.py"
apk_package="com.flexycore.caffeinemark"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
