#! /bin/bash
echo "file;algo;taille anneau;nb robots;error;time elapsed" > ../data/data-time.csv
for file in `ls ../logs/log-time | grep algo`
do
    ctrl=0
    echo -n "$file;" >> ../data/data-time.csv
    if [ `echo $file | grep -c 'algov5'` == 0 ]
    then
        echo -n "7;" >> ../data/data-time.csv
    else
        echo -n "5;" >> ../data/data-time.csv
    fi
    echo -n "`sed -r -n 's/^taille_anneau =  (.*)$/\1/p' ../logs/log-time/$file`;" >> ../data/data-time.csv
    echo -n "`sed -r -n 's/^nb_robots =  (.*)$/\1/p' ../logs/log-time/$file`;" >> ../data/data-time.csv
    if [ `grep -c 'Command exited with non-zero status 1' ../logs/log-time/$file` == 1 ]
    then
        echo -n "1;" >> ../data/data-time.csv
        let "ctrl+=1"
        echo "Error with $file"
    fi
    if [ `grep -c 'Command terminated by signal' ../logs/log-time/$file` == 1 ]
    then
        echo -n "2;" >> ../data/data-time.csv
        let "ctrl+=1"
        echo "Error with $file"
    fi
    if [ $ctrl == 0 ]
    then
        echo -n "0;" >> ../data/data-time.csv
    fi
    echo "`sed -r -n 's/^.*elapsed : (.*)$/\1/p' ../logs/log-time/$file`" >> ../data/data-time.csv
done