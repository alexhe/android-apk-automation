#!/bin/bash
# Author: Botao Sun <botao.sun@linaro.org>

function get_raw_logcat(){
    adb logcat > $1 2>&1 &
    raw_logcat_pid=$!
    echo "Raw logcat output transfer in progress..."
    sleep 120
    echo "Raw logcat output transfer finished!"
    if [ -n "${raw_logcat_pid}" ]; then
        kill -9 ${raw_logcat_pid}
    fi
}

get_raw_logcat "logcat_gearses1eclair.txt"
