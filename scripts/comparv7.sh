#! /bin/bash
export TIME="%C\n\tReal time elapsed : %E\n"
FAIL=0
toKill=0
for robot in {2..5}
do
    echo "robot = $robot" > tmpComparv7.txt
    for taille in {2..10}
    do
        echo "taille : $taille | nb robot : $robot" > ../log/log-time-phiUltimate24/log_algov7_${taille}_${robot}.txt
        echo "Init + phiUltimate" >> ../log/log-time-phiUltimate24/log_algov7_${taille}_${robot}.txt
        /usr/bin/time -a -o ../log/log-time-phiUltimate24/log_algov7_${taille}_${robot}.txt python3 main.py $taille $robot 7 >> ../log/log-time-phiUltimate24/log_algov7_${taille}_${robot}.txt &
    done
    jobs -l >> tmpComparv7.txt
    if [ $toKill -gt 0 ]
    then
        kill -9 $toKill
    fi
    ./killer.sh tmpComparv7.txt $robot &
    toKill=`jobs -l | sed -r -n 's/^.* ([0-9]+) En.*killer.*$/\1/p'`
    while read line
    do
        if [ `echo $line | grep -c 'algov7'` -gt 0 ]
        then
            wait `echo $line | sed -r -n 's/^.* ([0-9]+) En.*algov7.*$/\1/p'` || let "FAIL+=1"
        fi
    done < tmpComparv7.txt
    echo "nombre de FAIL : $FAIL"
done
kill -9 $toKill
rm -f tmpComparv7.txt