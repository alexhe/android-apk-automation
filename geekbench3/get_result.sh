#!/bin/bash
# Author: Botao Sun <botao.sun@linaro.org>

function get_result(){
    echo "Geekbench test result transfer in progress..."
    adb pull $1 $2
    if [ $? -ne 0 ]; then
        echo "Test result transfer failed!"
        return 1
    else
        echo "Test result transfer finished!"
        # Rename the file, should be only one .gb3 file on target directory
        mv *.gb3 geekbench3_result.gb3
        if [ $? -ne 0 ]; then
            echo "File rename failed! There should be only one .gb3 file under the current directory!"
            return 1
        else
            echo "Test result file for Geekbench 3 now is geekbench3_result.gb3"
            return 0
        fi
    fi
}

get_result "/data/data/com.primatelabs.geekbench3/files" "./"
