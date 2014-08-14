#!/bin/sh

SCORE=`awk -F'[][]' '/SBGlobal.nProductivityIndex/{k=$2}END{print k}' logcat.log`
echo "Score is: $SCORE"
lava-test-case SmartbenchScore --result pass --measurement $SCORE
