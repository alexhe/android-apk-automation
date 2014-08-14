#!/bin/bash

#need to be defined for different benchmark apks
activity="com.jeffboody.GearsES1eclair/.GearsES1eclair"
apk_file_name="GearsES1eclair-20110501.apk"
test_method="python vc.py"
apk_package="com.jeffboody.GearsES1eclair"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
