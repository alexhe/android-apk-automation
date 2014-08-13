#!/bin/bash

#need to be defined for different benchmark apks
activity="com.antutu.ABenchMark/.ABenchMarkStart"
apk_file_name="antutu_benchmark_4.0.3.apk"
test_method="python vc.py"
apk_package="com.antutu.ABenchMark"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"




