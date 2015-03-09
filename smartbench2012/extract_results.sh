#!/bin/bash

local_this_parent="$(cd $(dirname $0);pwd)"
source "${local_this_parent}/../common/common.sh"
source "${local_this_parent}/../common/statistic_average.sh"

SCORE=`awk -F'[][]' '/SBGlobal.nProductivityIndex/{k=$2}END{print k}' ${F_LOGCAT}`
UNIT="points"

echo "Score is: $SCORE"
output_test_result SmartbenchScore pass $SCORE $UNIT
