#!/bin/bash

#need to be defined for different benchmark apks
activity="com.antutu.ABenchMark/.ABenchMarkStart"
apk_file_name="com.antutu.ABenchMark-1.apk"
test_method="python vc.py"
apk_package="com.antutu.ABenchMark"

function change_no_update(){
    user=`adb shell ls -l /data/data/|grep com.antutu.ABenchMark|cut -d \  -f 2`
    user=`echo ${user}|sed 's/\r//'`
    dir_prefs="/data/data/com.antutu.ABenchMark/shared_prefs"
    adb push ${parent_dir}/shared_prefs "${dir_prefs}"
    adb shell chown ${user}:${user} "${dir_prefs}"
    adb shell chmod 700 "${dir_prefs}"
    adb shell chown ${user}:${user} "${dir_prefs}/com.antutu.ABenchMark_preferences.xml"
    adb shell chmod 660 "${dir_prefs}/com.antutu.ABenchMark_preferences.xml"
}

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
post_install="change_no_update"
main "$@"
