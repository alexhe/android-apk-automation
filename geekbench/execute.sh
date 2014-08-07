#!/bin/bash

#need to be defined for different benchmark apks
activity="ca.primatelabs.geekbench2/.HomeActivity"
apk_file_name="ca.primatelabs.geekbench2-1.apk"
test_method="python vc.py"
apk_package="ca.primatelabs.geekbench2"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
