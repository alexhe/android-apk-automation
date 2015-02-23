#!/bin/bash

#need to be defined for different benchmark apks
apk_package="net.danielroggen.scimark"
activity="${apk_package}/.ActivityMain"
apk_file_name="03-SciMark.apk"
test_method="python vc.py"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"

base_url="http://testdata.validation.linaro.org/apks/JavaBenchmark/non-pure-java-benchmarks/"

main "$@"
