#!/bin/bash

#need to be defined for different benchmark apks
activity="com.wtsang02.sqliteutil.activities/.MainActivity"
apk_file_name="com.redlicense.benchmark.sqlite-1.apk"
test_method="python vc.py"
apk_package="com.wtsang02.sqliteutil.activities"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
