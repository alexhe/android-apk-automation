#!/bin/bash

#need to be defined for different benchmark apks
activity="com.antutu.ABenchMark/.ABenchMarkStart"
apk_file_name="AnTuTuBenchmark5.6.2.apk"
test_method="python vc.py"
apk_package="com.antutu.ABenchMark"
antutu562_64bit_apk_name="AnTuTu_Benchmark_64-bit_5.6.apk"

#following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"

func_post_uninstall_antutu562(){
    package_64bit="com.antutu.benchmark.bench64"
    func_kill_uninstall "${antutu562_64bit_apk_name}" "${package_64bit}"
}

func_post_install_antutu562(){
    package_64bit="com.antutu.benchmark.bench64"
    func_kill_uninstall "${antutu562_64bit_apk_name}" "${package_64bit}"
    if adb shell getprop ro.product.cpu.abilist |grep -q "arm64-v8a"; then
        if get_file_with_base_url "${antutu562_64bit_apk_name}" "${BASE_URL}" "${D_APKS}"; then
            adb install -r "${D_APKS}/${antutu562_64bit_apk_name}"
            if [ $? -ne 0 ]; then
                echo "Failed to install ${antutu562_64bit_apk_name}."
                return 1
            fi
        else
            echo "Failed to get ${antutu562_64bit_apk_name}."
            return 1
        fi

    fi
}
post_uninstall="func_post_uninstall_antutu562"
post_install="func_post_install_antutu562"
timeout="20m"
main "$@"
