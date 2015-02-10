#!/bin/bash

local_this_file_path="${BASH_SOURCE[0]}"
local_this_parent_dir=$(cd $(dirname ${local_this_file_path}); pwd)
source ${local_this_parent_dir}/common/common2.sh
source ${local_this_parent_dir}/common/statistic_average.sh

## override default value in common2.sh
G_LOOP_COUNT=12
BASE_URL="http://testdata.validation.linaro.org/apks/JavaBenchmark/pure-java-applications"
#BASE_URL="scp://testdata//home/testdata.validation.linaro.org/apks/JavaBenchmark/pure-java-applications"
APPS="NULL,com.android.browser/.BrowserActivity,Browser"
APPS="${APPS} NULL,com.android.settings/.Settings,Settings"
APPS="${APPS} 01-3D_Volcano_Island.apk,com.omnigsoft.volcanoislandjava/.App,3D_Volcano_Island"
APPS="${APPS} 02-com.blong.jetboy_1.0.1.apk,com.blong.jetboy/.JetBoy,JetBoy"
APPS="${APPS} 03-HelloEffects.apk,com.example.android.mediafx/.HelloEffects,HelloEffects"
APPS="${APPS} 04-FREEdi_YouTube_Player_v2.2.apk,tw.com.freedi.youtube.player/.MainActivity,FREEdi_YouTube_Player"
APPS="${APPS} 17-GooglePlayBooks.apk,com.google.android.apps.books/.app.BooksActivity,GooglePlayBooks"
APPS="${APPS} 46-Zedge.apk,net.zedge.android/.activity.ControllerActivity,Zedge"
APPS="${APPS} 55-ShootBubbleDeluxe.apk,com.shootbubble.bubbledexlue/.FrozenBubble,ShootBubbleDeluxe"
G_APPS=${APPS}

## Contants for this script
dir_rawdata="${D_RAWDATA}"
dir_apks="${D_APKS}"
f_starttime="${dir_rawdata}/activity_starttime.raw"
f_mem="${dir_rawdata}/activity_mem.raw"
f_cpu="${dir_rawdata}/activity_cpu.raw"
f_procrank="${dir_rawdata}/activity_procrank.raw"
f_stat="${dir_rawdata}/activity_stat.raw"
f_procmem="${dir_rawdata}/activity_procmem.raw"
f_maps="${dir_rawdata}/activity_maps.raw"
f_dumpsys_mem="${dir_rawdata}/activity_dumpsys_meminfo.raw"
f_smaps="${dir_rawdata}/activity_smaps.raw"

f_res_starttime="${dir_rawdata}/activity_starttime.csv"
f_res_mem="${dir_rawdata}/activity_mem.csv"
f_res_cpu="${dir_rawdata}/activity_cpu.csv"
f_res_procrank="${dir_rawdata}/activity_procrank.csv"
f_res_dumpsys_mem="${dir_rawdata}/activity_dumpsys_meminfo.csv"
f_result="${dir_rawdata}/result.csv"

# only called by collect_mem_raw_data
collect_raw_procmem_data(){
    echo "===package=${loop_app_package}, count=${loop_count} start" >> "${f_procmem}"
    adb shell su 0 procmem ${pid} >> "${f_procmem}"
    echo "===package=${loop_app_package}, count=${loop_count} end" >> "${f_procmem}"

    echo "===package=${loop_app_package}, count=${loop_count} start" >> "${f_procmem}_p"
    adb shell su 0 procmem -p ${pid} >> "${f_procmem}_p"
    echo "===package=${loop_app_package}, count=${loop_count} end" >> "${f_procmem}_p"

    echo "===package=${loop_app_package}, count=${loop_count} start" >> "${f_procmem}_m"
    adb shell su 0 procmem -m ${pid} >> "${f_procmem}_m"
    echo "===package=${loop_app_package}, count=${loop_count} end" >> "${f_procmem}_m"
}


collect_mem_raw_data(){
    # get memory info
    adb shell ps|grep "${loop_app_package}" >>"${f_mem}"
    adb shell su 0 procrank|grep "${loop_app_package}" >> "${f_procrank}"

    echo "===package=${loop_app_package}, count=${loop_count} start" >> "${f_dumpsys_mem}"
    adb shell su 0 dumpsys meminfo "${loop_app_package}" >> "${f_dumpsys_mem}"
    echo "===package=${loop_app_package}, count=${loop_count} end" >> "${f_dumpsys_mem}"

    local pid=$(adb shell ps|grep ${loop_app_package}|awk '{print $2}')
    if [ -n "${pid}" ]; then
        adb shell su 0 cat /proc/${pid}/stat >> "${f_stat}"
        echo "===package=${loop_app_package}, count=${loop_count} start" >> "${f_maps}"
        adb shell su 0 cat /proc/${pid}/maps >> "${f_maps}"
        echo "===package=${loop_app_package}, count=${loop_count} end" >> "${f_maps}"

        echo "===package=${loop_app_package}, count=${loop_count} start" >> "${f_smaps}"
        adb shell su 0 cat /proc/${pid}/smaps >> "${f_smaps}"
        echo "===package=${loop_app_package}, count=${loop_count} end" >> "${f_smaps}"
        collect_raw_procmem_data
    fi
}

func_post_install_app_bench(){
    func_post_install
    # catch the cpu information before start activity
    cpu_time_before=$(adb shell cat /proc/stat|grep 'cpu '|tr -d '\n')
}

func_pre_uninstall_app_bench(){
    # get cpu information
    cpu_time_after=$(adb shell cat /proc/stat|grep 'cpu '|tr -d '\n')
    echo "${loop_app_package},${cpu_time_before},${cpu_time_after}" >>"${f_cpu}"

    # get activity start time information
    adb logcat -d|grep "Displayed ${loop_app_start_activity}" >>"${f_starttime}"

    collect_mem_raw_data

    func_pre_uninstall
}

func_post_uninstall_app_bench(){
    func_post_uninstall
    echo "" >>"${f_starttime}"
    echo "" >>"${f_mem}"
    echo "" >>"${f_cpu}"
}

format_starttime_raw_data(){
    if [ ! -f "${f_starttime}" ]; then
        return
    fi
    sed '/^\s*$/d' "${f_starttime}" |tr -s ' '|tr -d '\r'|sed 's/^.*Displayed\ //'|sed 's/(.*$//' |sed 's/: +/,/' >"${f_res_starttime}.tmp"
    for line in $(cat "${f_res_starttime}.tmp"); do
        local app_pkg=$(echo $line|cut -d, -f1)
        local app_time=$(echo $line|cut -d, -f2|sed 's/ms//g')
        # assumed no minute here
        if echo $app_time|grep -q 's'; then
            local app_sec=$(echo $app_time|cut -ds -f1)
            local app_msec=$(echo $app_time|cut -ds -f2)
            app_time=$((app_sec * 1000 + app_msec))
        fi
        echo "${app_pkg},${app_time}" >>"${f_res_starttime}"
    done
    rm -f "${f_res_starttime}.tmp"
}

format_mem_raw_data(){
    if [ ! -f "${f_mem}" ]; then
        return
    fi
    sed '/^\s*$/d' "${f_mem}" |tr -s ' '|tr -d '\r'|awk '{printf "%s,%s,%s\n", $9, $4, $5;}' >"${f_res_mem}"
}

calculate_field_value(){
    local line_val=$1 && shift
    local field_no=$1 && shift
    [ -z "${line_val}" ] && return
    [ -z "${field_no}" ] && return

    local val1=$(echo "${line_val}"|cut -d, -f${field_no})
    local field2_no=$(echo "${field_no}+10"|bc)
    local val2=$(echo "${line_val}"|cut -d, -f${field2_no})
    local val=$(echo "${val2}-${val1}"|bc)
    echo "${val}"
}

format_cputime(){
    local f_data=$1 && shift
    if ! [ -f "$f_data" ]; then
        return
    fi
    rm -fr "${f_data}_2nd"
    for line in $(cat "${f_data}"); do
        if ! echo "$line"|grep -q ,; then
            continue
        fi
        local key=$(echo $line|cut -d, -f1)

        local val_user=$(calculate_field_value "$line" 2)
        local val_nice=$(calculate_field_value "$line" 3)

        local val_system=$(calculate_field_value "$line" 4)
        local val_idle=$(calculate_field_value "$line" 5)
        local val_io_wait=$(calculate_field_value "$line" 6)
        local val_irq=$(calculate_field_value "$line" 7)
        local val_softirq=$(calculate_field_value "$line" 8)

        local val_total_user=$(echo "scale=2; ${val_user}+${val_nice}"|bc)
        local val_total_system=$(echo "scale=2; ${val_system}+${val_irq}+${val_softirq}"|bc)
        local val_total_idle=$val_idle
        local val_total_iowait=$val_io_wait
        local val_total=$(echo "scale=2; ${val_total_system}+${val_total_user}+${val_total_idle}+${val_total_iowait}"|bc)

        local percent_user=$(echo "scale=2; $val_total_user*100/$val_total"|bc)
        local percent_sys=$(echo "scale=2; $val_total_system*100/$val_total"|bc)
        local percent_idle=$(echo "scale=2; $val_total_idle*100/$val_total"|bc)
        echo "$key,$percent_user,$percent_sys,$percent_idle" >> "${f_data}_2nd"
    done
}

format_cpu_raw_data(){
    if [ ! -f "${f_cpu}" ]; then
        return
    fi
    sed '/^\s*$/d' "${f_cpu}" |tr -d '\r'|tr -s ' '|tr ' ' ','|sed 's/cpu,//g' >"${f_res_cpu}"
    format_cputime "${f_res_cpu}"
}

format_procrank_data(){
    if [ ! -f "${f_procrank}" ]; then
        return
    fi
    sed '/^\s*$/d' "${f_procrank}" |sed 's/^\s*//'|tr -d '\r'|awk '{printf("%s,%s,%s,%s,%s\n", $6, $2, $3, $4, $5)}'|tr -d 'K'>"${f_res_procrank}"
}

format_procmem_data(){
    if [ ! -f "${f_procmem}" ]; then
        return
    fi
    sed 's/^\s*//' "${f_procmem}" |tr -s ' '|tr ' ' ',' >"${f_procmem}.csv"
    sed 's/^\s*//' "${f_procmem}_p" |tr -s ' '|tr ' ' ',' >"${f_procmem}_p.csv"
    sed 's/^\s*//' "${f_procmem}_m" |tr -s ' '|tr ' ' ',' >"${f_procmem}_m.csv"
}

format_dumpsys_meminfo(){
    if [ ! -f "${f_dumpsys_mem}" ]; then
        return
    fi
    local package=""
    local native=""
    local dalvik=""
    local sommap=""
    #===package=com.android.browser, count=0 start
    #       Native Heap     5981     5916        0        0     7864     7183      680
    #       Dalvik Heap     6839     6520        0        0    19304    11701     760
    #        .so mmap    12434      212    11052        0
    #        TOTAL    46946    20720    21524        0    29861    29539    15543
    for line in $(grep -e start -e TOTAL -e "Native Heap" -e "Dalvik Heap" -e ".so mmap" ${f_dumpsys_mem}|tr '=' ','|tr ' ' ','|tr -s ','|tr -d '\r'|sed 's/^,//') ; do
        case "X${line}" in
            "Xpackage"*)
                if [ -n "${package}" ] && [ -n "${native}" ] \
                   && [ -n "${dalvik}" ] && [ -n "${sommap}" ]  && [ -n "${total}" ]; then
                    echo "${package},${native},${dalvik},${sommap},${total}" >>"${f_res_dumpsys_mem}"
                fi
                package=$(echo "${line}"|cut -d\, -f2)
                ;;
            "XNative,Heap"*)
                native=$(echo "${line}"|cut -d\, -f3)
                ;;
            "XDalvik,Heap"*)
                dalvik=$(echo "${line}"|cut -d\, -f3)
                ;;
            "X.so,mmap"*)
                sommap=$(echo "${line}"|cut -d\, -f3)
                ;;
            "XTOTAL"*)
                total=$(echo "${line}"|cut -d\, -f2)
                ;;
            "X"*)
                continue
                ;;
        esac
    done
    if [ -n "${package}" ] && [ -n "${native}" ] \
       && [ -n "${dalvik}" ] && [ -n "${sommap}" ]  && [ -n "${total}" ]; then
        echo "${package},${native},${dalvik},${sommap},${total}" >>"${f_res_dumpsys_mem}"
    fi
}

format_raw_data(){
    rm -fr ${f_res_starttime} ${f_res_mem} ${f_res_cpu} ${f_res_procrank} ${f_res_dumpsys_mem}

    format_starttime_raw_data
    format_mem_raw_data
    format_cpu_raw_data
    format_procrank_data
    format_dumpsys_meminfo
}

set_browser_homepage(){
    pref_file="com.android.browser_preferences.xml"
    pref_dir="/data/data/com.android.browser/shared_prefs/"
    pref_content='<?xml version="1.0" encoding="utf-8" standalone="yes" ?>
<map>
    <boolean name="enable_hardware_accel_skia" value="false" />
    <boolean name="autofill_enabled" value="true" />
    <string name="homepage">about:blank</string>
    <boolean name="last_paused" value="false" />
    <boolean name="debug_menu" value="false" />
</map>'

    # start browser for the first time to genrate preference file
    adb shell am start -W -S com.android.browser/.BrowserActivity
    user_grp=$(adb shell su 0 ls -l "${pref_dir}/${pref_file}"|awk '{printf "%s:%s", $2, $3}')
    func_kill_uninstall "NULL" "com.android.browser"

    echo "${pref_content}" > "${pref_file}"
    adb push "${pref_file}" "/data/local/tmp/${pref_file}"
    adb shell su 0 cp "/data/local/tmp/${pref_file}" "${pref_dir}/${pref_file}"
    adb shell su 0 chown ${user_grp} "${pref_dir}/${pref_file}"
    adb shell su 0 chmod 660 "${pref_dir}/${pref_file}"

    adb shell am start -W -S com.android.browser/.BrowserActivity
    func_kill_uninstall "NULL" "com.android.browser"
    adb shell am start -W -S com.android.browser/.BrowserActivity
    func_kill_uninstall "NULL" "com.android.browser"
}

func_prepare_app_bench(){
    func_prepare_environment

    if echo "$APPS"|grep -q "com.android.browser"; then
        set_browser_homepage
    fi
    rm -fr "${f_starttime}" "${f_mem}" "${f_cpu}" "${f_procrank}" "${f_stat}" "${f_procmem}" "${f_procmem}_m" "${f_procmem}_p"
}

statistic_data(){
    rm -fr "${f_result}"
    statistic "$f_res_starttime" 2|sed "s/^/starttime_/"|sed "s/$/ ms/"| tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_mem}" 2|sed "s/^/ps_vss_/" |sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_mem}" 3|sed "s/^/ps_rss_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_procrank}" 2|sed "s/^/procrank_vss_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_procrank}" 3|sed "s/^/procrank_rss_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_procrank}" 4|sed "s/^/procrank_pss_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_procrank}" 5|sed "s/^/procrank_uss_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_dumpsys_mem}" 2|sed "s/^/dumpsys_meminfo_pss_native_heap_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_dumpsys_mem}" 3|sed "s/^/dumpsys_meminfo_pss_dalvik_heap_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_dumpsys_mem}" 4|sed "s/^/dumpsys_meminfo_pss_sommap_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_dumpsys_mem}" 5|sed "s/^/dumpsys_meminfo_pss_total_/"|sed "s/$/ KB/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_cpu}_2nd" 2|sed "s/^/cpu_user_/"|sed "s/$/ %/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_cpu}_2nd" 3|sed "s/^/cpu_sys_/"|sed "s/$/ %/"|tee -a "${f_result}"
    echo "--------------------------------"
    statistic "${f_res_cpu}_2nd" 4|sed "s/^/cpu_idle_/"|sed "s/$/ %/"|tee -a "${f_result}"
    sed -i 's/=/,/' "${f_result}"
}


func_post_test_app_bench(){
    format_raw_data
    statistic_data
}

main(){
    var_func_parse_parameters=""
    var_func_prepare_environment="func_prepare_app_bench"
    var_func_post_test="func_post_test_app_bench"

    var_func_pre_install=""
    var_func_post_install="func_post_install_app_bench"
    var_func_run_test=""
    var_test_command=""
    var_func_pre_uninstall="func_pre_uninstall_app_bench"
    var_func_post_uninstall="func_post_uninstall_app_bench"
    common_main "$@"
}

main "$@"
