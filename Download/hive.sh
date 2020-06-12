#!/bin/bash

#processedfilelist=`hive -S -e "select tableA.file_name from $1.tableA;"`
processedfilelist=`hive -S -e "select t.file_names from (SELECT file_names FROM $2.tableB lateral view explode(tableB.filename) exploded as file_names) as t join $1.tableA on t.file_names=tableA.file_name;"`
arr=()

for processedfiles in $processedfilelist; do
    IFS=',' read -ra processedfile <<< "$processedfiles"
    for filepath in "${processedfile[@]}"; do
        #echo "$filepath"
        arr+=( "$filepath" )
    done
done

echo "${arr[@]}"
