#! /bin/bash
sleep 86400
robot=`sed -r -n 's/^robot = (.*)$/\1/p' $1`
if [ $robot == $2 ]
then
    while read line
    do
        if [ `echo $line | grep -c 'algo'` == 1 ]
        then
            process=`echo $line | sed -r -n 's/^.* ([0-9]+) En.*algo.*$/\1/p'`
            pkill -9 -P $process
            # kill -9 $process
        fi
    done < $1
fi