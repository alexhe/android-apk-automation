#!/bin/bash

#need to be defined for different benchmark apks
apk_package="com.eembc.coremark"
activity="${apk_package}/.tabs"
apk_file_name="02-AndEBench2014.apk"
test_method="python vc.py"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"

base_url="http://testdata.validation.linaro.org/apks/JavaBenchmark/non-pure-java-benchmarks/"

main "$@"
