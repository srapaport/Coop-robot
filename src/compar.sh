#! /bin/bash
export TIME="%C\n\tReal time elapsed : %E\n"
for robot in {2..5}
do
    for taille in {2..12}
    do
        echo "taille : $taille | nb robot : $robot" #> test_log/log_${taille}_${robot}.txt
        echo "Init + phiSimple" > test_log/log_algov5_${taille}_${robot}.txt
        echo "Init + phiSimple" > test_log/log_algov7_${taille}_${robot}.txt
        /usr/bin/time -a -o test_log/log_algov5_${taille}_${robot}.txt python3 algov5.py $taille $robot >> test_log/log_algov5_${taille}_${robot}.txt & /usr/bin/time -a -o test_log/log_algov7_${taille}_${robot}.txt python3 algov7.py $taille $robot >> test_log/log_algov7_${taille}_${robot}.txt
    done
done