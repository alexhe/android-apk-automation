#!/bin/bash

local_common_file_path="${BASH_SOURCE[0]}"
local_common_parent_dir=$(cd $(dirname ${local_common_file_path}); pwd)
source ${local_common_parent_dir}/common2.sh

base_url="http://testdata.validation.linaro.org/apks/"
post_install=""
pre_uninstall=""
ret_value=0
timeout=10m

f_tmp_governor="/data/local/tmp/governor.txt"
func_cleanup(){
    adb shell "cat ${f_tmp_governor} > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    adb shell "cat ${f_tmp_governor} > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor"
    adb shell rm ${f_tmp_governor}
    func_kill_uninstall "RotationOff.apk" "rotation.off"
}

func_install_start_RotationAPK(){
    local apk_name="RotationOff.apk"
    local apk_path="${D_APKS}/RotationOff.apk"
    if [ -f "${apk_path}" ]; then
        echo "The file(${apk_path}) already exists."
    else
        get_file_with_base_url "${apk_name}" "${base_url}" "${D_APKS}"
    fi
    adb shell pm list packages | grep rotation.off
    if [ $? -ne 0 ]; then
        adb install "${apk_path}"
    fi
    sleep 2
    adb shell am start 'rotation.off/.RotationOff'
    sleep 2
}

function init(){

    func_install_start_RotationAPK

    adb shell "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor > ${f_tmp_governor}"
    adb shell "echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    adb shell "echo performance > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor"
}

func_prepare_benchmark(){
    init
    echo "init done"

    func_prepare_environment
}

func_run_test_bench(){
    local test_script="${D_ROOT}/${loop_app_name}/vc.py"
    local ret
    if [ -f "${test_script}" ]; then
        local test_command="python ${test_script}"
        if [ -n "${var_test_command_timeout}" ]; then
            timeout ${var_test_command_timeout} ${test_command}
            ret=$?
            if [ $ret -eq 124 ]; then
                echo  "Time out to run ${test_command}: ${var_test_command_timeout}"
            fi
        else
            ${test_command}
            ret=$?
        fi
        sleep 5
        return $ret
    fi
}

func_post_uninstall_bench(){
    func_post_uninstall
    if [ -n "${post_uninstall}" ]; then
        ${post_uninstall}
    fi
}

function main(){
    echo "test timeout: ${timeout}"
    parent_dir=$(cd ${parent_dir}; pwd)
    export parent_dir=${parent_dir}

    var_func_parse_parameters=""
    var_func_prepare_environment="func_prepare_benchmark"
    var_func_post_test="func_cleanup"

    var_func_pre_install=""
    var_func_post_install="${post_install}"
    var_func_run_test="func_run_test_bench"
    var_test_command=""
    var_test_command_timeout="${timeout}"
    var_func_pre_uninstall="${pre_uninstall}"
    var_func_post_uninstall="func_post_uninstall_bench"

    G_APPS="${apk_file_name},${activity},$(basename ${parent_dir})"
    BASE_URL="${base_url}"
    common_main "$@"

    return ${ret_value}
}
