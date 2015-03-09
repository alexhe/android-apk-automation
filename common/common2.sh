#!/bin/bash

local_common2_file_path="${BASH_SOURCE[0]}"
local_common2_parent_dir=$(cd $(dirname ${local_common2_file_path}); pwd)
D_ROOT=$(cd $(dirname ${local_common2_parent_dir}); pwd)

D_RAWDATA="${D_ROOT}/rawdata"
D_APKS="${D_ROOT}/apks"
F_RAWDAT_ZIP="${D_ROOT}/rawdata.zip"

F_LOGCAT="${D_RAWDATA}/logcat.log"
F_LOGCAT_EVENTS="${D_RAWDATA}/logcat-events.log"
D_STREAMLINE="${D_RAWDATA}/streamline"
D_SCREENSHOT="${D_RAWDATA}/screenshots"

COLLECT_STREAMLINE=false
SERIAL=""
G_APPS=""
G_LOOP_COUNT=1
BASE_URL=""

## Description:
##    get specified the apk file from remote
## Usage:
##    get_file_with_base_url $remote_relative_path $base_url $target_dir
## Example:
##    get_file_with_base_url "${apk_apk}" "${BASE_URL}" "${D_APKS}"
get_file_with_base_url(){
    local remote_rel_path=$1 && shift
    base_name=$(basename ${remote_rel_path})
    local base_url=$1 && shift
    local target_dir=$1 && shift

    if [ -z "${remote_rel_path}" ]; then
        echo "The file name must be specified."
        return 1
    fi

    if [ -z "${base_url}" ]; then
        echo "The file name must be specified."
        return 1
    fi

    if [ -z "${target_dir}" ]; then
        echo "The file name must be specified."
        return 1
    fi

    if [ -f "${target_dir}/${base_name}" ]; then
        echo "The file(${remote_rel_path}) already exists."
        return 0
    fi
    mkdir -p "${target_dir}"
    case "X${base_url}" in
        "Xscp://"*)
            # like scp://yongqin.liu@testdata.validation.linaro.org/home/yongqin.liu
            apk_url="${base_url}/${remote_rel_path}"
            url_no_scp=`echo ${apk_url}|sed 's/^\s*scp\:\/\///'|sed 's/\//\:\//'`
            scp "${url_no_scp}" "${target_dir}/${base_name}"
            if [ $? -ne 0 ]; then
                echo "Failed to get the apk(${remote_rel_path}) with ${base_url}"
                return 1
            fi
            ;;
        "Xssh://"*)
            git clone "${base_url}" "${target_dir}"
            if [ $? -ne 0 ]; then
                echo "Failed to get the apks with ${base_url}"
                return 1
            fi
            ;;
        "Xhttp://"*)
            wget "${base_url}/${remote_rel_path}" -O "${target_dir}/${base_name}"
            if [ $? -ne 0 ]; then
                echo "Failed to get the apks with ${base_url}"
                return 1
            fi
            ;;
        "X"*)
            echo "Failed to get the file($remote_rel_path)."
            echo "The schema of the ${base_url} is not supported now!"
            return 1
            ;;
    esac

    return 0
}

## Description:
##    used to kill the process for the specified process name
## Usage:
##    kill_process $process_name_pattern
## Example:
##    kill_process "gatord"
kill_process(){
    local proc=$1 && shift
    [ -z "${proc}" ] && return

    while adb shell ps | grep -q -E "\s+${proc}\s+"; do
        local pid=$(adb shell ps|grep -E "\s+${proc}\s+"|awk '{print $2}')
        if [ -n "${pid}" ]; then
            adb shell su 0 kill -9 "${pid}"
        fi
    done
    sleep 5
}

## Description:
##   prepare environment for streamline and start the gatord
##   to collect streamline data
## Usage:
##    collect_streamline_data_before "${app_id}" "${timeout}"
## Example:
##    collect_streamline_data_before "Browser_0" "10"
## Note:
##   This function will do nothing if COLLECT_STREAMLINE is not set to true
collect_streamline_data_before(){
    if [ "X${COLLECT_STREAMLINE}" != "Xtrue" ]; then
        return
    fi
    local app_name=$1 && shift
    if [ -z "${app_name}" ];then
        return
    fi
    local gatord_timeout="${1-10}" && shift

    kill_process "gatord"
    adb shell su 0 rm -fr /data/local/tmp/streamline
    adb shell mkdir /data/local/tmp/streamline
    cat >session.xml <<__EOF__
<?xml version="1.0" encoding="US-ASCII" ?>
<session version="1" title="${app_name}" target_path="@F" call_stack_unwinding="yes" parse_debug_info="yes" high_resolution="no" buffer_mode="streaming" sample_rate="normal" duration="${gatord_timeout}">
</session>
__EOF__
    adb push session.xml /data/local/tmp/streamline/session.xml
    echo "Gatord starts:$(date)"
    adb shell "su 0 gatord -s /data/local/tmp/streamline/session.xml -o /data/local/tmp/streamline/${app_name}.apc" &
    adb shell sleep 2
}

## Description:
##    wait for the gatord finished or kill it if over the time specified in seconds
## Usage:
##    wait_kill_gatord_finish "${timeout}"
## Example:
##    wait_kill_gatord_finish "10"
wait_kill_gatord_finish(){
    local gatord_timeout="${1-10}" && shift
    local proc="gatord"
    local count=1
    while adb shell ps | grep -q -E "\s+${proc}\s+"; do
        count=$((count+1))
        if [ ${count} -gt ${gatord_timeout} ]; then
            local pid=$(adb shell ps|grep -E "\s+${proc}\s+"|awk '{print $2}')
            if [ -n "${pid}" ]; then
                adb shell su 0 kill -9 "${pid}"
                sleep 2
            fi
        else
            sleep 1
        fi
    done
}

## Description:
##    wait for the gatord daemon to finish, and
##    pull the collected streamline data to the specified directory
## Usage:
##    collect_streamline_data_post "${app_id}" "${target_dir}"
## Example:
##    collect_streamline_data_post "Browser_0" "streamline_data"
## Note:
##   This function will do nothing if COLLECT_STREAMLINE is not set to true
collect_streamline_data_post(){
    if [ "X${COLLECT_STREAMLINE}" != "Xtrue" ]; then
        return
    fi
    local app_name=$1 && shift
    if [ -z "${app_name}" ]; then
        return
    fi
    local target_dir=$1 && shift
    if [ -z "${target_dir}" ]; then
        echo "Please specify the target directory where to save the data file"
        return
    fi
    echo "Wait gatord to finish:$(date)"
    wait_kill_gatord_finish
    echo "Gatord findihed:$(date)"
    adb shell su 0 chown -R shell:shell data/local/tmp/streamline
    adb pull /data/local/tmp/streamline/${app_name}.apc ${target_dir}/${app_name}.apc
    #streamline -analyze ${capture_dir}
    #streamline -report -function ${apd_f} |tee ${parent_dir}/streamlineReport.txt
}

# uninstall or kill the running package
func_kill_uninstall(){
    local app_apk=$1 && shift
    local app_pkg=$1 && shift
    if [ "X${app_apk}" != "XNULL" ];then
        adb shell pm list packages | grep -q "${app_pkg}"
        if [ $? -eq 0 ]; then
            adb uninstall "${app_pkg}"
        fi
    else
        adb shell am force-stop "${app_pkg}"
    fi
}

func_pre_install(){
    # clean logcat buffer
    adb logcat -c
    adb logcat -b events -c
    sleep 3

    func_kill_uninstall "${loop_app_apk}" "${loop_app_package}"
}

func_post_install(){
    collect_streamline_data_before "${loop_app_name}_${loop_count}"
    adb shell am kill-all
    sleep 5
}

func_run_test(){
    if [ -n "${var_test_command}" ]; then
        timeout ${var_test_command_timeout} ${var_test_command}
        local ret=$?
        if [ $ret -eq 124 ]; then
           echo  "Time out to run ${var_test_command}: ${var_test_command_timeout}"
        fi
        sleep 5
        return $ret
    fi
}

func_pre_uninstall(){
    collect_streamline_data_post "${loop_app_name}_${loop_count}" "${D_STREAMLINE}"
    # capture screen shot
    adb shell screencap /data/local/tmp/app_screen.png
    adb pull /data/local/tmp/app_screen.png ${D_SCREENSHOT}/${loop_app_name}_${loop_count}.png
}

collect_raw_logcat_data(){
    echo "===package=${loop_app_package}, count=${loop_count} start" >> "${F_LOGCAT}"
    adb logcat -d -v time >> "${F_LOGCAT}"
    echo "===package=${loop_app_package}, count=${loop_count} end" >> "${F_LOGCAT}"
    echo "===ackage=${loop_app_package}, count=${loop_count} start" >> "${F_LOGCAT_EVENTS}"
    adb logcat -d -b events -v time >> "${F_LOGCAT_EVENTS}"
    echo "===package=${loop_app_package}, count=${loop_count} start" >> "${F_LOGCAT_EVENTS}"
}

func_post_uninstall(){
    collect_raw_logcat_data
}

## Description:
##    run test for the specified applications for the specified times
## Usage:
##    func_loop_apps_for_times $app_list $loop_times
##        app_list: space separated application list, each application should
##                  be specified as following format:
##                     apk_name,apk_package/start_activity_name,nickname
##                  like:
##                     03-JBench.apk,it.JBench.bench/it.JBench.jbench.MainActivity,JBench
##                  or:
##                      NULL,com.android.settings/.Settings,Settings
##                   NULL in the apk_name place holder means no need to install the application
##        loop_times: the count that the test should be run
## Example:
##        func_loop_apps_for_times "03-JBench.apk,it.JBench.bench/it.JBench.jbench.MainActivity,JBench NULL,com.android.settings/.Settings,Settings" 12
## Note:
##      var_func_pre_install
##      var_func_post_install
##      var_func_run_test
##      var_func_pre_uninstall
##      var_func_post_uninstall
##          variables of loop_app_apk/loop_app_start_activity/loop_app_package/loop_app_name/loop_count can be used in the above functions
func_loop_apps_for_times(){
    local loop_apps_list=$1 && shift
    local loop_apps_times=$1 && shift

    for apk in ${loop_apps_list}; do
        local loop_app_apk=$(echo $apk|cut -d, -f1)
        loop_app_apk=$(basename ${loop_app_apk})
        local loop_app_start_activity=$(echo $apk|cut -d, -f2)
        local loop_app_package=$(echo ${loop_app_start_activity}|cut -d\/ -f1)
        local loop_app_name=$(echo $apk|cut -d, -f3)
        local loop_count=0

        while [ ${loop_count} -lt ${loop_apps_times} ]; do
            ## steps before install the apk,
            ## like clean the logcat buffer or uninstall the application first
            ## in case failed to uninstall last time
            if [ -n "${var_func_pre_install}" ];then
                ${var_func_pre_install}
            else
                func_pre_install
            fi

            # install apk
            if [ "X${loop_app_apk}" != "XNULL" ];then
                adb install -r "${D_APKS}/${loop_app_apk}"
                if [ $? -ne 0 ]; then
                    echo "Failed to install ${loop_app_apk}."
                    return 1
                fi
            fi

            # run steps after install but before start the activiety
            # since for applications we need prepare something like configuration
            # so that to make the application work
            if [ -n "${var_func_post_install}" ]; then
               ${var_func_post_install}
            else
                func_post_install
            fi

            # start activity
            adb shell am start -W -S ${loop_app_start_activity}

            # run test steps after started the activity
            if [ -n "${var_func_run_test}" ]; then
                ${var_func_run_test}
            else
                func_run_test
            fi

            if [ -n "${var_func_pre_uninstall}" ]; then
               ${var_func_pre_uninstall}
            else
                func_pre_uninstall
            fi

            # uninstall or kill the app process
            func_kill_uninstall "${loop_app_apk}" "${loop_app_package}"

            if [ -n "${var_func_post_uninstall}" ]; then
               ${var_func_post_uninstall}
            else
                func_post_uninstall
            fi

            loop_count=$((loop_count + 1 ))
        done
    done
}

func_get_all_apks(){
    local loop_apps_list=$1 && shift
    for apk in ${loop_apps_list}; do
        local app_apk=$(echo $apk|cut -d, -f1)
        app_apk=$(echo "$app_apk"|sed 's/\s*$//' |sed 's/^\s*//')
        if [ -z "${app_apk}" ]; then
            echo "Either the apk file name or NULL must be specified for one application"
            echo "This application configuration is not valid: $apk"
            return 1
        fi
        if [ "X${app_apk}" = "XNULL" ]; then
            continue
        fi
        get_file_with_base_url "${app_apk}" "${BASE_URL}" "${D_APKS}"|| return 1
    done
    return 0
}

func_prepare_environment(){
    if [ -n "${SERIAL}" ];then
        ANDROID_SERIAL=$SERIAL
        export ANDROID_SERIAL
    else
        serial=`adb get-serialno|sed 's/\r//g'`
        if [ "X${serial}" == "Xunknown" ]; then
            echo "Can not get the serial number autotically,"
            echo "Please specify the serial number with the -s option"
            exit 1
        else
            export ANDROID_SERIAL=${serial}
        fi
    fi

    rm -fr ${D_RAWDATA}
    mkdir -p "${D_STREAMLINE}" "${D_SCREENSHOT}" "${D_APKS}"

    func_get_all_apks "$G_APPS"|| exit 1

    adb shell svc power stayon true
    adb shell input keyevent MENU
    adb shell input keyevent BACK
}

func_print_usage_common(){
    echo "$(basename $0) --base-url BASE_URL [--serial serial_no] [--loop-count LOOP_COUNT] [--streamline true|false] APP_CONFIG_LIST ..."
    echo "     --serial: specify serial number for the device"
    echo "     --base-url: specify the based url where the apks will be gotten from"
    echo "     --loop-count: specify the number that how many times should be run for each application to get the average result, default is 12"
    echo "     --streamline: specify if we need to collect the streamline data, true amd false can be specified, default is fasle"
    echo "     APP_CONFIG_LIST: specify the configurations for each application as following format:"
    echo "             APK_NAME,PACKAGE_NAME/APP_ACTIVITY,APP_NICKNAME"
    echo "         APK_NAME: the apk file name which we will get from the BASE_URL specified by --base-url option."
    echo "                   if NULL is specified, it means this APK is a system apk, no need to get from BASE_URL"
    echo "         APP_PACKAGE: the package name for this application"
    echo "         APP_ACTIVITY: the activity name will be started for this application"
    echo "         APP_NICKNAME: a nickname for this application, should only contain alphabet and digits"
}

func_parse_parameters_common(){
    local para_loop_count=""
    local para_apps=""
    while [ -n "$1" ]; do
        case "X$1" in
            X--base-url)
                BASE_URL=$2
                shift 2
                ;;
            X--streamline)
                COLLECT_STREAMLINE=$2
                shift 2
                ;;
            X--loop-count)
                para_loop_count=$2
                shift 2
                ;;
            X-s|X--serial)
                SERIAL=$2
                shift 2
                ;;
            X-h|X--help)
                func_print_usage_common
                exit 1
                ;;
            X-*)
                echo "Unknown option: $1"
                func_print_usage_common
                exit 1
                ;;
            X*)
                para_apps="${para_apps} $1"
                shift 1
                ;;
        esac
    done

    if [ -z "${BASE_URL}" ]; then
        echo "BASE_URL information must be specified."
        exit 1
    fi
    if [ -n "${para_loop_count}" ] && echo "${para_loop_count}"| grep -q -P '^\d+$'; then
        G_LOOP_COUNT=${para_loop_count}
    elif [ -n "${para_loop_count}" ]; then
        echo "The specified LOOP_COUNT(${para_loop_count}) is not valid"
        exit 1
    fi

    para_apps=$(echo "$para_apps"|sed 's/\s*$//' |sed 's/^\s*//')
    if [ -n "${para_apps}" ]; then
        G_APPS="${para_apps}"
    fi
}

## Description:
##    main function to run for all application tests, both normal acitivity start test
##    or benchmark things tests
## Usage:
##
## Example:
##
## Note:
##    all apks should be able to get with the same base url
##    var_func_parse_parameters
##    var_func_prepare_environment
##    var_func_post_test
common_main(){
    if [ -n "${var_func_parse_parameters}" ]; then
        ${var_func_parse_parameters} "$@"
        if [ $? -ne 0 ]; then
            echo "Failed to parse the parameters!"
            if [ -n "${var_func_usage}" ]; then
                ${var_func_usage}
            fi
            exit 1
        fi
    else
       func_parse_parameters_common
    fi

    if [ -n "${var_func_prepare_environment}" ]; then
        "${var_func_prepare_environment}"
        if [ $? -ne 0 ]; then
            echo "Failed to prepare the environment!"
            exit 1
        fi
    else
        func_prepare_environment
    fi

    func_loop_apps_for_times "${G_APPS}" "${G_LOOP_COUNT}"

    if [ -n "${var_func_post_test}" ]; then
        "${var_func_post_test}"
        if [ $? -ne 0 ]; then
            echo "Failed to do actions after the test!"
            exit 1
        fi
    fi

    rm -fr "${F_RAWDAT_ZIP}"
    local old_pwd=$(pwd)
    local d_zip_dir="$(dirname ${D_RAWDATA})"
    local d_zip_name="$(basename ${D_RAWDATA})"
    cd ${d_zip_dir};
    zip -r "${F_RAWDAT_ZIP}" "${d_zip_name}"
    cd ${old_pwd}
    echo "Please reference the file ${F_RAWDAT_ZIP} for all the raw data."
}
