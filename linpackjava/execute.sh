#!/bin/bash

#need to be defined for different benchmark apks
apk_package="com.LinpackJava"
activity="${apk_package}/.LinpackJavaActivity"
apk_file_name="02-LinpackJava.apk"
test_method="python vc.py"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"

base_url="http://testdata.validation.linaro.org/apks/JavaBenchmark/pure-java-benchmarks/"

main "$@"
