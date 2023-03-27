#! /bin/bash
cd /home/solal/Documents/Stage_lip6/Coop-robot/visualization
for dir in `ls ../logs/`
do
	if [ ! -d "./clean_$dir" ]
	then
		mkdir clean_$dir
	fi
	echo $dir
	for file in `ls ../logs/$dir`
	do
		path=$(readlink -f ../logs/$dir/$file)
		if [ `echo -n $file | grep -c "algov7"` == 1 ] && !([ `cat $path | grep -c 'Tiemout reached'` -eq 1 ] || [ `cat $path | grep -c 'Command terminated by signal'` == 1 ])
		then
			echo $path
			ring_size=`cat $path | sed -r -n 's/^taille_anneau = (.*)$/\1/p'`
			nb_robots=`cat $path | sed -r -n 's/^nb_robots = +([0-9]*)$/\1/p'`
			loop_size=`cat $path | sed -r -n 's/^.*len\(pk.*([0-9]+)$/\1/p'`
			python3 visualization.py $path $ring_size $nb_robots $loop_size > ./clean_$dir/clean_$file
		fi
	done
done