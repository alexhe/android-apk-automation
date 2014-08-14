#!/bin/bash

#need to be defined for different benchmark apks
activity="com.glbenchmark.glbenchmark27/net.kishonti.gfxbench.GfxMainActivity"
apk_file_name="com.glbenchmark.glbenchmark-3D-benchmark.apk"
test_method="python vc.py"
apk_package="com.glbenchmark.glbenchmark27"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
