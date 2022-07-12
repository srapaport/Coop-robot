#! /bin/bash
export TIME="%C\n\tReal time elapsed : %E\n"
FAIL=0
for robot in {2..5}
do
    for taille in {2..10}
    do
        echo "taille : $taille | nb robot : $robot" &
        echo "Init + phiSimple" > ../log/log-time-phiSM/log_algov5_${taille}_${robot}.txt
        /usr/bin/time -a -o ../log/log-time-phiSM/log_algov5_${taille}_${robot}.txt python3 algov5.py $taille $robot >> ../log/log-time-phiSM/log_algov5_${taille}_${robot}.txt &
    done
    for job in `jobs -p`
    do
        wait $job || let "FAIL+=1"
    done
    echo "nombre de FAIL : $FAIL"
done