#!/bin/bash

#need to be defined for different benchmark apks
apk_package="com.eembc.andebench"
activity="com.eembc.andebench/.splash"
apk_file_name="andebench-pro.apk"
test_method="python vc.py"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"

function get_result(){
    local host_csv_f="${D_RAWDATA}/andebench.log.csv"
    adb pull /mnt/sdcard/Download/andebench.log.csv "${host_csv_f}"
    sed -i 's/ /_/g' "${host_csv_f}"
    sed -i 's/(\|)//g' "${host_csv_f}"
    local regex="^CoreMark-HPC|^Memory Bandwidth,|^Memory Latency,|^Storage,|^Platform,|^3D,|^Overall"
    for line in $(grep -P "${regex}" ${host_csv_f}); do
        local field1=$(echo $line|cut -d, -f1)
        local field2=$(echo $line|cut -d, -f2)
        local field3=$(echo $line|cut -d, -f3)

        local key=""
        local value=""
        local result=""
        local units=""
        if [ -z "${field3}" ]; then
            key="${field1}"
            value="${field2}"
        else
            key="${field1}_${field2}"
            value="${field3}"
        fi
        old_value="${value}"
        if echo "${old_value}"|grep -q -P '\d$'; then
            value="${old_value}"
            units="points"
            result="pass"
        elif [ "X${old_value}" = "XNA" ];then
            result="fail"
        else
            value=$(echo ${old_value}|tr -d "[:alpha:]/")
            units=$(echo ${old_value}|tr -d "[:digit:].")
            result="pass"
        fi
        if [ "X${result}" = "Xpass" ]; then
            output_test_result "andebenchpro_${key}" "pass" "${value}" "${units}"
        else
            output_test_result "andebenchpro_${key}" "fail"
        fi
    done
}
pre_uninstall="get_result"
main "$@"
