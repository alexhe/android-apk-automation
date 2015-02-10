#!/bin/bash

#need to be defined for different benchmark apks
activity="com.smartbench.twelve/.Smartbench2012"
apk_file_name="Smartbench2012.apk"
test_method="python vc.py"
apk_package="com.smartbench.twelve"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
post_uninstall="${parent_dir}/extract_results.sh"
main "$@"
