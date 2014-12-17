#!/bin/bash
# Author: Milosz Wasilewski <milosz.wasilewski@linaro.org>

# need to be defined for different benchmark apks
activity="com.quicinc.vellamo/.main.MainActivity"
apk_file_name="com.quicinc.vellamo-3.apk"
test_method="python vc.py"
apk_package="com.quicinc.vellamo"

# following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
