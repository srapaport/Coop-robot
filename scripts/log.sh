#! /bin/bash
echo "Cration du csv pour les logs $1"
echo "file;algo;taille anneau;nb robots;error;time elapsed" > ../data/data-$1/data-time.csv
for file in `ls ../logs/log-time-$1 | grep algo`
do
    ctrl=0
    echo -n "$file;" >> ../data/data-$1/data-time.csv
    if [ `echo $file | grep -c 'algov5'` == 0 ]
    then
        echo -n "7;" >> ../data/data-$1/data-time.csv
    else
        echo -n "5;" >> ../data/data-$1/data-time.csv
    fi
    echo -n "`sed -r -n 's/^taille : (.*) \|.*$/\1/p' ../logs/log-time-$1/$file`;" >> ../data/data-$1/data-time.csv
    echo -n "`sed -r -n 's/^taille : (.*) \| nb robot : (.*)$/\2/p' ../logs/log-time-$1/$file`;" >> ../data/data-$1/data-time.csv
    if [ `grep -c 'Command exited with non-zero status 1' ../logs/log-time-$1/$file` == 1 ]
    then
        echo -n "1;;" >> ../data/data-$1/data-time.csv
        echo "`sed -r -n 's/^.*elapsed : (.*)$/\1/p' ../logs/log-time-$1/$file`" >> ../data/data-$1/data-time.csv
        let "ctrl+=1"
        echo "Error with $file"
    fi
    if [ `grep -c 'Command terminated by signal' ../logs/log-time-$1/$file` == 1 ]
    then
        echo "2;24:00:00" >> ../data/data-$1/data-time.csv
        let "ctrl+=1"
    fi
    if [ `grep -c 'Tiemout reached' ../logs/log-time-$1/$file` == 1 ]
    then
        echo "3;24:00:00" >> ../data/data-$1/data-time.csv
        let "ctrl+=1"
    fi
    if [ $ctrl == 0 ]
    then
        echo -n "0;" >> ../data/data-$1/data-time.csv
        echo "`sed -r -n 's/^.*elapsed : (.*)$/\1/p' ../logs/log-time-$1/$file`" >> ../data/data-$1/data-time.csv
    fi
done