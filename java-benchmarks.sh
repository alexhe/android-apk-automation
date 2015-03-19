#!/bin/bash

local_file_path="${BASH_SOURCE[0]}"
local_parent_dir=$(cd $(dirname ${local_file_path}); pwd)
source ${local_parent_dir}/common/common.sh
source ${local_parent_dir}/common/statistic_average.sh

base_url="http://testdata.validation.linaro.org/apks/"
#base_url="scp://testdata//home/testdata.validation.linaro.org/apks"
timeout=120m

func_post_uninstall_smartbench2012(){
    ${local_parent_dir}/smartbench2012/extract_results.sh
}
function func_post_uninstall_bench_batch(){
    func_post_uninstall
    if [ "X${loop_app_name}" = "Xsmartbench2012" ]; then
        func_post_uninstall_smartbench2012
    fi
}

function local_main(){
    echo "test timeout: ${timeout}"
    parent_dir=$(cd ${parent_dir}; pwd)
    export parent_dir=${parent_dir}

    var_func_parse_parameters=""
    var_func_prepare_environment="func_prepare_benchmark"
    var_func_post_test="func_cleanup"

    var_func_pre_install=""
    var_func_post_install="${post_install}"
    var_func_run_test="func_run_test_bench"
    var_test_command=""
    var_test_command_timeout="${timeout}"
    var_func_pre_uninstall="${pre_uninstall}"
    var_func_post_uninstall="func_post_uninstall_bench_batch"

    G_APPS="${G_APPS} JavaBenchmark/pure-java-benchmarks/01-Java_Whetstone.apk,com.roywhet/.JavaWhetstoneActivity,javawhetstone"
    G_APPS="${G_APPS} JavaBenchmark/pure-java-benchmarks/03-JBench.apk,it.JBench.bench/it.JBench.jbench.MainActivity,jbench"
    G_APPS="${G_APPS} JavaBenchmark/pure-java-benchmarks/02-LinpackJava.apk,com.LinpackJava/.LinpackJavaActivity,linpackjava"
    G_APPS="${G_APPS} JavaBenchmark/non-pure-java-benchmarks/03-SciMark.apk,net.danielroggen.scimark/.ActivityMain,scimark"
    G_APPS="${G_APPS} JavaBenchmark/non-pure-java-benchmarks/02-AndEBench2014.apk,com.eembc.coremark/.tabs,andebench2014"
    G_APPS="${G_APPS} gr.androiddev.BenchmarkPi-1.apk,gr.androiddev.BenchmarkPi/.BenchmarkPi,benchmarkpi"
    G_APPS="${G_APPS} com.greenecomputing.linpack-1.apk,com.greenecomputing.linpack/.Linpack,linpack"
    G_APPS="${G_APPS} Smartbench2012.apk,com.smartbench.twelve/.Smartbench2012,smartbench2012"
    G_LOOP_COUNT=12
    BASE_URL="${base_url}"
    common_main "$@"

    return ${ret_value}
}

local_main "$@"
