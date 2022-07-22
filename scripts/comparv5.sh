#! /bin/bash
export TIME="%C\n\tReal time elapsed : %E\n"
FAIL=0
toKill=0
for robot in {2..5}
do
    echo "robot = $robot" > tmpComparv5.txt
    for taille in {2..10}
    do
        echo "taille : $taille | nb robot : $robot" > ../log/log-time-phiUltimate24/log_algov5_${taille}_${robot}.txt
        echo "Init + phiUltimate" >> ../log/log-time-phiUltimate24/log_algov5_${taille}_${robot}.txt
        /usr/bin/time -a -o ../log/log-time-phiUltimate24/log_algov5_${taille}_${robot}.txt python3 algov5.py $taille $robot >> ../log/log-time-phiUltimate24/log_algov5_${taille}_${robot}.txt &
    done
    jobs -l >> tmpComparv5.txt
    if [ $toKill -gt 0 ]
    then
        kill -9 $toKill
    fi
    ./killer.sh tmpComparv5.txt $robot &
    toKill=`jobs -l | sed -r -n 's/^.* ([0-9]+) En.*killer.*$/\1/p'`
    while read line
    do
        if [ `echo $line | grep -c 'algov5'` -gt 0 ]
        then
            wait `echo $line | sed -r -n 's/^.* ([0-9]+) En.*algov5.*$/\1/p'` || let "FAIL+=1"
        fi
    done < tmpComparv5.txt
    echo "nombre de FAIL : $FAIL"
done
kill -9 $toKill
rm -f tmpComparv5.txt