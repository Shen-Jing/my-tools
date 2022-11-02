#!/usr/bin/zsh

# Example: ${script} -p ${src_path} -t 2022-11-01-1027
while getopts p:t: flag
do
    case "${flag}" in
        p) prefix=${OPTARG};;
        t) timestamp=${OPTARG};;
    esac
done

cat "${prefix}_unanalyzed_yours" > ~/diffs/fail/${timestamp}
cat "${prefix}_system_failure"  >> ~/diffs/fail/${timestamp}
