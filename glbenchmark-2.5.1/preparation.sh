#!/bin/bash
# Author: Botao Sun <botao.sun@linaro.org>

local_this_parent="$(cd $(dirname $0);pwd)"
${local_this_parent}/file_transfer.sh
sleep 2

python ${local_this_parent}/glbenchmark_first_launch.py
sleep 2
