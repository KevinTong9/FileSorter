#!/bin/bash
lmter=500
find ./ -type f > tempfile1.temp
cat tempfile1.temp | grep '/\.git/' | sed 's/\/\.git\/.*//g' | sort | uniq | sed 's/ /\\ /' | tr '\r\n' '\n' > tempfile2.temp
rm mv ./log.ini ./${RANDOM}_log.ini
sed 's/^\(.*\)$/7z a -t7z -bb3 \1.7z \1 2\>\&1 | tee -a log.ini \;if \[ \"$?\" -eq 0 \] \; then echo success \&\& rm -rvf \1 2\>\&1 \| tee -a log.ini \;fi/g' ./tempfile2.temp > tempfile3.temp ;chmod +x ./tempfile3.temp ; ./tempfile3.temp
sed 's/.*\/\.git\/.*//g' ./tempfile1.temp  | tr '\r\n' '\n' | tr '\n\n' '\n' > tempfile4.temp
sed 's/[^\/]*$//g' tempfile4.temp | sort | uniq -c > tempfile5.temp
sed 's/[^\/]*$//g' tempfile4.temp | sort | uniq > tempfile6.temp
cat ./tempfile6.temp | while read line;do echo -n $line ; cat tempfile5.temp | grep "$line" | awk '{sum += $1};END {print sum}' ;done | tee tempfile7.temp
cat tempfile7.temp | while read line;do num=$(echo $line|sed 's/^.*\///g');path=$(echo $line | sed 's/\/[0-9]\+$//g');if [ "$num" -gt "$lmter" ] ; then echo $path $num;fi;done | grep \/ |tee tempfile8.temp
grep "\/" tempfile8.temp | sed 's/ \+[0-9]\+$//g'> tempfile9.temp
cp tempfile9.temp result.txt && rm ./*.temp
