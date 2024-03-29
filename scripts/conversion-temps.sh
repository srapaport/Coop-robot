#! /bin/bash
echo "file;algo;taille anneau;nb robots;error;time elapsed" > ../data/data-$1/data-timev2.csv
for data in `cat ../data/data-$1/data-time.csv`
do
    echo -n $data | sed -r -n 's/(^.*algo.*;).*:.*$/\1/p' >> ../data/data-$1/data-timev2.csv
    if [ `echo -n $data | grep -c 'algov'` == 1 ]
        then
        if [ `echo -n $data | grep -E -c '^.*;(.*):(.*)\.(.*)$'` == 1 ]
        then
            hour=0
            min=`echo $data | sed -r -n 's/^.*;(.*):(.*)\.(.*)$/\1/p'`
            sec=`echo $data | sed -r -n 's/^.*;(.*):0?(.+)\.(.*)$/\2/p'`
            milli=`echo $data | sed -r -n 's/^.*;(.*):(.*)\.0?([1-9]?[0-9]{1})$/\3/p'`
        else
            hour=`echo $data | sed -r -n 's/^.*;(.*):(.*):(.*)$/\1/p'`
            min=`echo $data | sed -r -n 's/^.*;(.*):0?(.+):(.*)$/\2/p'`
            sec=`echo $data | sed -r -n 's/^.*;(.*):(.*):0?([1-9]?[0-9]{1})$/\3/p'`
            milli=0
        fi
        timeRes=$(((60*60*$hour) + (60*$min) + $sec))
        #echo " $hour h: $min min: $sec s. $milli"
        echo $timeRes.$milli >> ../data/data-$1/data-timev2.csv
    fi
done