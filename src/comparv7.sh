#! /bin/bash
export TIME="%C\n\tReal time elapsed : %E\n"
FAIL=0
taille=2
for robot in {2..5}
do
    echo "taille : $taille | nb robot : $robot"
    echo "Init + phiSimple" > ../log/log_algov7_${taille}_${robot}.txt
    echo "Init + phiSimple" > ../log/log_algov7_$((taille + 1))_${robot}.txt
    echo "Init + phiSimple" > ../log/log_algov7_$((taille + 2))_${robot}.txt
    echo "Init + phiSimple" > ../log/log_algov7_$((taille + 3))_${robot}.txt
    echo "Init + phiSimple" > ../log/log_algov7_$((taille + 4))_${robot}.txt
    echo "Init + phiSimple" > ../log/log_algov7_$((taille + 5))_${robot}.txt
    echo "Init + phiSimple" > ../log/log_algov7_$((taille + 6))_${robot}.txt
    echo "Init + phiSimple" > ../log/log_algov7_$((taille + 7))_${robot}.txt
    echo "Init + phiSimple" > ../log/log_algov7_$((taille + 8))_${robot}.txt
    /usr/bin/time -a -o ../log/log_algov7_${taille}_${robot}.txt python3 algov7.py $taille $robot >> ../log/log_algov7_${taille}_${robot}.txt &
    /usr/bin/time -a -o ../log/log_algov7_$((taille + 1))_${robot}.txt python3 algov7.py $((taille + 1)) $robot >> ../log/log_algov7_$((taille + 1))_${robot}.txt &
    /usr/bin/time -a -o ../log/log_algov7_$((taille + 2))_${robot}.txt python3 algov7.py $((taille + 2)) $robot >> ../log/log_algov7_$((taille + 2))_${robot}.txt &
    /usr/bin/time -a -o ../log/log_algov7_$((taille + 3))_${robot}.txt python3 algov7.py $((taille + 3)) $robot >> ../log/log_algov7_$((taille + 3))_${robot}.txt &
    /usr/bin/time -a -o ../log/log_algov7_$((taille + 4))_${robot}.txt python3 algov7.py $((taille + 4)) $robot >> ../log/log_algov7_$((taille + 4))_${robot}.txt &
    /usr/bin/time -a -o ../log/log_algov7_$((taille + 5))_${robot}.txt python3 algov7.py $((taille + 5)) $robot >> ../log/log_algov7_$((taille + 5))_${robot}.txt &
    /usr/bin/time -a -o ../log/log_algov7_$((taille + 6))_${robot}.txt python3 algov7.py $((taille + 6)) $robot >> ../log/log_algov7_$((taille + 6))_${robot}.txt &
    /usr/bin/time -a -o ../log/log_algov7_$((taille + 7))_${robot}.txt python3 algov7.py $((taille + 7)) $robot >> ../log/log_algov7_$((taille + 7))_${robot}.txt &
    /usr/bin/time -a -o ../log/log_algov7_$((taille + 8))_${robot}.txt python3 algov7.py $((taille + 8)) $robot >> ../log/log_algov7_$((taille + 8))_${robot}.txt &
    for job in `jobs -p`
    do
        wait $job || let "FAIL+=1"
    done
    echo "nombre de FAIL : $FAIL"
done