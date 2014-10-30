#!/bin/bash

#need to be defined for different benchmark apks
activity="com.jeffboody.GearsES2eclair/.GearsES2eclair"
#apk_file_name="GearsES2eclair-20110501.apk"
apk_file_name="GearsES2eclair-20141021.apk"
test_method="python vc.py"
apk_package="com.jeffboody.GearsES2eclair"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
