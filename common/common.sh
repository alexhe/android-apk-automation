#!/bin/bash

#base_url="ssh://linaro-lava@linaro-private.git.linaro.org/srv/linaro-private.git.linaro.org/qa/benchmark-apks.git"
base_url="http://people.linaro.org/~milosz.wasilewski/apks/"
png_dir_device="/data/local/tmp/"
post_install=""
pre_uninstall=""
do_streamline=false
ret_value=0
timeout=10m

#function install_linaro_android_jar(){
#    jar_name="linaro.android.jar"
#    tgt_path="/data/local/tmp/${jar_name}"
#    jar_url="http://testdata.validation.linaro.org/tools/${jar_name}"
#    exist=`adb shell "ls ${tgt_path} 2>/dev/null"`
#    if [ -z "${exist}" ]; then
#        wget ${jar_url} -O ${jar_name}
#        adb push ${jar_name} ${tgt_path}
#        rm -f ${jar_name}
#    fi
#}

function delete_png_files_on_device(){
    png_dir=${1-$png_dir_device}
    png_files=`adb shell "ls ${png_dir}/*.png 2>/dev/null"`
    for png_f in ${png_files}; do
        png_f=`echo ${png_f}|sed 's/\r//'`
        adb shell rm "${png_f}"
    done
}

function pull_png_files_from_device(){
    src_dir_device=${1-"${png_dir_device}"}
    tgt_dir_local=${2-"${parent_dir}"}
    png_files=`adb shell "ls ${png_dir}/*.png 2>/dev/null"`
    for png_f in ${png_files}; do
        png_f=`echo ${png_f}|sed 's/\r//'`
        adb pull "${png_f}" "${tgt_dir_local}" &>/dev/null
    done
}

function init(){
    # uninstall the apk application
    # don't uninstall if apk file name is empty
    if [ ! -z "$apk_file_name" ]; then
        echo "trying to unistall ${apk_package}"
        adb uninstall "${apk_package}"
        echo "unistalled ${apk_package}"
    fi
    # clear the logcat information
    adb logcat -c
    sleep 5

    rm -fr "${parent_dir}"/*.png 2>/dev/null
    delete_png_files_on_device "${png_dir_device}"

    disableRotationapk="${APKS_DIR}/RotationOff.apk"
    if [ -f "{$disableRotationapk}" ]; then
        echo "The file(${disableRotationapk}) already exists."
    else
        get_file_with_base_url "RotationOff.apk"
    fi
    adb shell pm list packages | grep rotation.off
    if [ $? -ne 0 ]; then
        adb install "${disableRotationapk}"
    fi
    sleep 2
    adb shell am start 'rotation.off/.RotationOff'
    sleep 2
    adb shell "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor > /data/governor.txt"
    adb shell "echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    adb shell "echo performance > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor"
    adb shell logcat -c
    adb shell setprop ro.debug.drawtext true
    adb shell setprop ro.debug.textview true
    adb shell setprop ro.debug.loadDataWithBaseURL true
    logcat_file="${parent_dir}/logcat.log"
    echo "---------------------------------------------------"
    echo "A new test is started:`date`" |tee -a "${logcat_file}"
    adb logcat >>${logcat_file} &
    export LOGCAT_PID=$!
}


function cleanup(){
    adb shell "cat /data/governor.txt > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"
    adb shell "cat /data/governor.txt > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor"
    adb shell rm /data/governor.txt
    adb shell setprop ro.debug.drawtext false
    adb shell setprop ro.debug.textview false
    adb shell setprop ro.debug.loadDataWithBaseURL false
    adb uninstall rotation.off
    if [ -n "${LOGCAT_PID}" ]; then
        kill -9 ${LOGCAT_PID}
    fi
}

function export_serial(){
    serial="${1}" && shift
    if [ -n "${serial}" ]; then
        export ANDROID_SERIAL=${serial}
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
}

function export_parent_dir(){
    old_pwd=`pwd`
    cd ${parent_dir}
    parent_dir=`pwd`
    cd ${old_pwd}
    export parent_dir=${parent_dir}
}

function export_apks_dir(){
    #export APKS_DIR="${parent_dir}/../benchmark-apks"
    export APKS_DIR="${parent_dir}"
}

function get_file_with_base_url(){
    file_name="${1}" && shift

    if [ -z "${file_name}" ]; then
        echo "File name must be passed!"
        exit 1
    fi

    if [ -f "${APKS_DIR}/${file_name}" ]; then
        echo "The file(${APKS_DIR}/${file_name}) already exists."
        return
    fi
    if [[ "${base_url}" =~ "scp://" ]]; then
        mkdir -p "${APKS_DIR}"
        apk_url="${base_url}/${file_name}"
        url_no_scp=`echo ${apk_url}|sed 's/^\s*scp\:\/\///'|sed 's/\//\:\//'`
        scp "${url_no_scp}" "${APKS_DIR}/${file_name}"
        if [ $? -ne 0 ]; then
            echo "Failed to get the apk(${file_name}) with ${base_url}"
            exit 1
        fi
    elif [[ "${base_url}" =~ "ssh://" ]]; then
        rm -fr "${APKS_DIR}"
        git clone "${base_url}" "${APKS_DIR}"
        if [ $? -ne 0 ]; then
            echo "Failed to get the apks with ${base_url}"
            exit 1
        fi
    elif [[ "${base_url}" =~ "http://" ]]; then
        mkdir -p "${APKS_DIR}"
        wget "${base_url}"/${file_name} -O "${APKS_DIR}"/${file_name}
        if [ $? -ne 0 ]; then
            echo "Failed to get the apks with ${base_url}"
            exit 1
        fi
    else
        echo "Failed to get the file($file_name)."
        echo "The schema of the ${base_url} is not supported now!"
        exit 1
    fi
}

function install_run_uninstall(){
    #install the apk files
    if [ ! -z "$apk_file_name" ]; then
        apk_file="${APKS_DIR}/${apk_file_name}"
        adb install "${apk_file}"
        if [ $? -ne 0 ]; then
            echo "Failed to install ${apk_file}."
            exit 1
        fi
    else
        # force stop activity if apk is already installed
        echo "stopping ${apk_package}"
        adb shell am force-stop "${apk_package}"
        sleep 5
    fi
    if [ -n "${post_install}" ]; then
        ${post_install}
    fi
    adb shell am start "${activity}"
    sleep 5
    adb shell am kill-all
    sleep 5
    streamline_init_capture
    if [ -n "${test_method}" ]; then
        timeout ${timeout} ${test_method}
        ret_value=$?
    fi
    sleep 5
    streamline_end_capture
    if [ -n "${pre_uninstall}" ]; then
        ${pre_uninstall}
    fi

    if [ ! -z "$apk_file_name" ]; then
        adb uninstall "${apk_package}"
    else
        # force stop activity if apk is a stock app
        echo "stopping ${apk_package}"
        adb shell am force-stop "${apk_package}"
        sleep 5
    fi
}

function collect_log(){
    sleep 5
    adb logcat -d -s "TextView" >${parent_dir}/logcat_textview.log
    sleep 5
    adb logcat -d -s "Canvas" >${parent_dir}/logcat_canvas.log
    sleep 5
    adb logcat -d -s "WebViewClassic.loadDataWithBaseURL" >${parent_dir}/logcat_webview.log
    sleep 5
}

function streamline_locate(){
    which streamline >&/dev/null
    return $?
}

function streamline_init_capture(){
    if ! ${do_streamline}; then
        return
    fi
    if ! streamline_locate; then
        echo "There is no streamline command found."
        echo "Please check your environment variable or install it"
        return
    fi

    echo "Start Streamline Capture.. "
    adb shell "rm -r /data/streamline 2>/dev/null"
    adb shell mkdir /data/streamline
    session_file="${parent_dir}/session.xml"
    adb push $session_file /data/streamline
    app_name=`basename $parent_dir`
    adb shell "gatord -s /data/streamline/session.xml -o /data/streamline/${app_name}.apc &"
    adb shell sleep 2
}

function streamline_end_capture(){
    if ! ${do_streamline}; then
        return
    fi
    if ! streamline_locate; then
        return
    fi

    echo "End Streamline Capture.. "
    ps_info=`adb shell ps -x | grep -E '\s+gatord\s+'`
    ##TODO maybe have multiple lines here
    pid=`echo $ps_info|cut -d \  -f 2|sed 's/\r//'`
    if [ -n "${pid}" ]; then
        adb shell kill $pid
    fi

    echo "Start Processing Streamline data."
    app_name=`basename $parent_dir`
    capture_dir="$parent_dir/${app_name}.apc"
    rm -fr ${capture_dir}
    adb pull /data/streamline/${app_name}.apc $capture_dir
    if [ $? -ne 0 ]; then
        echo "Failed to pull the streamline data from android!"
        exit 1
    fi
    streamline -analyze ${capture_dir}
    if [ $? -ne 0 ]; then
        echo "Failed to analyze the streamline data!"
        exit 1
    fi
    apd_f="${app_name}.apd"
    streamline -report -function ${apd_f} |tee ${parent_dir}/streamlineReport.txt
    if [ $? -ne 0 ]; then
        echo "Failed to generate the streamline report!"
        exit 1
    fi
    ##TODO detail parse should be done in run.py
    rm -fr ${capture_dir}
    adb shell rm -r /data/streamline
}
function show_usage(){
    echo "`basename $0` [--base-url|-b <base-url>] [<device-serial>] [--streamline]"
    echo "`basename $0` --help|-h"
}

function parse_arguments(){
    while test -n "$1"; do
        case "$1" in
            --help|-h)
                show_usage
                exit 1
                ;;
            --streamline|-s)
                do_streamline=true
                shift 1
                ;;
            "--base-url"|-b)
                if [ -z "$2" ]; then
                    show_usage
                    exit 1
                else
                    base_url="$2"
                    shift 2
                fi
                ;;
            *)
                if [ -n "${arg_serial}" ]; then
                    echo "Too many arguments are given!"
                    show_usage
                    exit 1
                fi
                arg_serial="$1"
                shift 1
                ;;
        esac
    done
}

function main(){
    echo ${test_timeout}
    arg_serial=""
    parse_arguments "$@"
    echo "parsing done"
    export_serial "${arg_serial}"
    export_parent_dir
    export_apks_dir
    echo "exports done"
    init
    echo "init done"
    if [ ! -z "$apk_file_name" ]; then
        get_file_with_base_url "${apk_file_name}"
    fi
    install_run_uninstall
    echo "testing done"
    pull_png_files_from_device "${png_dir_device}" ${parent_dir}
    collect_log
    cleanup
    return ${ret_value}
}
