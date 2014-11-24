#!/bin/bash
# Author: Botao Sun <botao.sun@linaro.org>

function get_cached_result(){
    echo "Cached result transfer in progress..."
    adb pull $1 $2
    if [ $? -ne 0 ]; then
        echo "Cached result transfer failed!"
        return 1
    else
        echo "Cached result transfer finished!"
        return 0
    fi
}

get_cached_result "/data/data/com.glbenchmark.glbenchmark25/cache/last_results_2.5.1.xml" "last_results_2.5.1.xml"
