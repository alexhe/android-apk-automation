#!/bin/bash

# need to be defined for different benchmark apks
activity="com.android.gallery3d/.app.GalleryActivity"
apk_file_name=""
test_method="python vc.py"
apk_package="com.android.gallery3d"

# following should no need to modify
parent_dir=`dirname ${0}`
source "${parent_dir}/../common/common.sh"
main "$@"
