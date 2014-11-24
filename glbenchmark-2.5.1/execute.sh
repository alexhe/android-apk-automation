#!/bin/bash

# need to be defined for different benchmark apks
activity="com.glbenchmark.glbenchmark25/com.glbenchmark.activities.GLBenchmarkDownloaderActivity"
apk_file_name="GLBenchmark_2.5.1.apk"
excluded_test_suite="C24Z24MS4"
# The first added parameter has been reserved by Android View Client.
# In order to add customised parameter, the first one must be the serial number from ADB
if [ -z "$1" ]; then
    device_serial_number=`adb get-serialno`
else
    device_serial_number=$1
fi
test_method="python vc.py $device_serial_number $excluded_test_suite"
apk_package="com.glbenchmark.glbenchmark25"

# following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
post_install="${parent_dir}/preparation.sh"
timeout=45m
main "$@"
