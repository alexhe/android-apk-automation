#!/bin/bash

#Required for N7 even after rooting 
adb shell chmod 777 /data/data/com.quicinc.vellamo/files/latest_result.html

#Pull results from device
adb pull /data/data/com.quicinc.vellamo/files/latest_result.html . 

if [ $? -ne 0 ]; then
    echo "Failed to get the result of vellamo test"
    exit 1
