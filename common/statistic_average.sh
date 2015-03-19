#!/bin/bash

## Description:
##    output the max value of the passed 2 parameters
## Usage:
##    f_max "${val1}" "${val2}"
## Example:
##    max=$(f_max "1.5" "2.0")
f_max(){
    local val1=$1
    local val2=$2
    [ -z "$val1" ] && echo $val2
    [ -z "$val2" ] && echo $val1

    local compare=$(echo "$val1>$val2"|bc)
    if [ "X$compare" = "X1" ];then
        echo $val1
    else
        echo $val2
    fi
}

## Description:
##    output the min value of the passed 2 parameters
## Usage:
##    f_min "${val1}" "${val2}"
## Example:
##    min=$(f_min "1.5" "2.0")
f_min(){
    local val1=$1
    local val2=$2
    [ -z "$val1" ] && echo $val1
    [ -z "$val2" ] && echo $val2

    local compare=$(echo "$val1<$val2"|bc)
    if [ "X$compare" = "X1" ];then
        echo $val1
    else
        echo $val2
    fi
}

## Description:
##   calculate the average value for specified csv file.
##   The first field of that csv file should be the key/name of that line,
##   Lines have the same key should be together.
## Usage:
##    statistic "${csv_file_path}" "${file_number}"
## Example:
##    statistic "$f_res_starttime" 2
## Note:
##    if less than 4 samples for that key/item there, average will be calculated as total/count
##    if 4 or more samples for that key/item there, average will be calculated with max and min excluded
statistic(){
    local f_data=$1
    if ! [ -f "$f_data" ]; then
        return
    fi
    local field_no=$2
    if [ -z "$field_no" ]; then
        field_no=2
    fi
    local total=0
    local max=0
    local min=0
    local old_key=""
    local new_key=""
    local count=0
    for line in $(cat "${f_data}"); do
        if ! echo "$line"|grep -q ,; then
            continue
        fi
        new_key=$(echo $line|cut -d, -f1)
        value=$(echo $line|cut -d, -f${field_no})
        if [ "X${new_key}" = "X${old_key}" ]; then
            total=$(echo "scale=2; ${total}+${value}"|bc -s)
            count=$(echo "$count + 1"|bc)
            max=$(f_max "$max" "$value")
            min=$(f_min "$min" "$value")
        else
            if [ "X${old_key}" != "X" ]; then
                if [ $count -ge 4 ]; then
                    average=$(echo "scale=2; ($total-$max-$min)/($count-2)"|bc)
                else
                    average=$(echo "scale=2; $total/$count"|bc)
                fi
                echo "$old_key=$average"
            fi
            total="${value}"
            max="${value}"
            min="${value}"
            old_key="${new_key}"
            count=1
        fi
    done
    if [ "X${new_key}" != "X" ]; then
        if [ $count -ge 4 ]; then
            average=$(echo "scale=2; ($total-$max-$min)/($count-2)"|bc)
        else
            average=$(echo "scale=2; $total/$count"|bc)
        fi
        echo "$new_key=$average"
    fi
}
