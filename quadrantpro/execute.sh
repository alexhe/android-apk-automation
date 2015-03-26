#!/bin/bash

#need to be defined for different benchmark apks
apk_package="com.aurorasoftworks.quadrant.ui.professional"
activity="${apk_package}/.QuadrantProfessionalLauncherActivity"
apk_file_name="com.aurorasoftworks.quadrant.ui.professional-1.apk"
test_method="python vc.py"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"

get_result(){
    local local_f_logcat="${D_RAWDATA}/quadrandpro.logcat"
    adb logcat -d >${local_f_logcat}
    for line in $(grep 'aggregate score is' ${local_f_logcat}|cut -d: -f2|sed 's/aggregate score is//g'|tr -s ' '|sed 's/^ //'|tr ' ' ','); do
        line=$(echo $line|sed 's/\r//g')
        key=$(echo $line|cut -d, -f1)
        value=$(echo $line|cut -d\,  -f2)
        output_test_result "${key}" "pass" "${value}" "points"
    done 
}

pre_uninstall="get_result"
main "$@"
