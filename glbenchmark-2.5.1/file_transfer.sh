#!/bin/bash
# Author: Botao Sun <botao.sun@linaro.org>
# Transfer obb and pre-config file from host to target device

obb_basic_path="/storage/sdcard0/Android"
config_basic_path="/data/data/com.glbenchmark.glbenchmark25"
errorword="No such"

function push_obb(){
    if [ ! -f $1 ]; then
        echo "Unable to find obb file!"
        return 1
    fi

    adb shell ls $obb_basic_path | grep "$errorword"

    if [ $? -eq 0 ]; then
        echo "$obb_basic_path does not exist on device!"
        return 1
    fi

    echo "File structure check OK! File transfer started..."
    adb push $1 $2

    if [ $? -ne 0 ]; then
        echo "obb file push failed!"
        return 1
    else
        echo "obb file pushed to device successfully!"
        return 0
    fi
}

function push_config(){
    if [ ! -f $1 ]; then
        echo "Unable to find config file!"
        return 1
    fi

    adb shell ls $config_basic_path | grep "$errorword"

    if [ $? -eq 0 ]; then
        echo "$config_basic_path does not exist on device!"
        return 1
    fi

    echo "File structure check OK! File transfer started..."
    adb push $1 $2

    if [ $? -ne 0 ]; then
        echo "Config file push failed!"
        return 1
    else
        echo "Config file pushed to device successfully!"
        return 0
    fi
}

push_obb "main.1.com.glbenchmark.glbenchmark25.obb" "$obb_basic_path/obb/com.glbenchmark.glbenchmark25/main.1.com.glbenchmark.glbenchmark25.obb"
push_config "com.glbenchmark.glbenchmark25_preferences.xml" "$config_basic_path/shared_prefs/com.glbenchmark.glbenchmark25_preferences.xml"
