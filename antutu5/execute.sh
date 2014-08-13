#!/bin/bash

#need to be defined for different benchmark apks
activity="com.antutu.ABenchMark5/.ABenchMarkStart"
apk_file_name="antutu-benchmark-v5-alpha.apk"
test_method="python vc.py"
apk_package="com.antutu.ABenchMark5"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"




