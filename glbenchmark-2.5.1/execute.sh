#!/bin/bash

# need to be defined for different benchmark apks
activity="com.glbenchmark.glbenchmark25/com.glbenchmark.activities.GLBenchmarkDownloaderActivity"
apk_file_name="GLBenchmark_2.5.1.apk"
apk_package="com.glbenchmark.glbenchmark25"

# following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
post_install="${parent_dir}/preparation.sh"
timeout=45m
main "$@"
