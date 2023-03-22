#! /bin/bash

file_log=$1

if [ $# -gt 0 ] && ([ `cat $file_log | grep -c 'Tiemout reached'` -eq 1 ] || [ `cat $file_log | grep -c 'Command terminated by signal'` == 1 ])
then
	exit 1
fi
nb_robots=0
size_ring=0
size_loop=0

while read line
do	
	if [ `echo $line | grep -c 'taille_anneau = '` == 1 ]
	then
		size_ring=`echo $line | sed -r -n 's/^taille_anneau = (.*)$/\1/p'`
	fi
	if [ `echo $line | grep -c 'nb_robots = '` == 1 ]
	then
		nb_robots=`echo $line | sed -r -n 's/^nb_robots = (.*)$/\1/p'`
	fi
	if [ `echo $line | grep -E -c '^k = '` == 1 ]
	then
		size_loop=`echo $line | sed -r -n 's/^k = .*([0-9]+)$/\1/p'`
		break
	fi
done < $file_log
echo	"(id robot, next moove, equity bit)" > res.txt
echo 	"Configuration initiale :" >> res.txt
cpt=0
while [ $cpt -ne $size_ring ]
do
	echo "p$cpt :" >> res.txt
	let "cpt+=1"
done

robot=0
pos_robot=0
next_move=0
equity_bit=0
while [ $robot -ne $nb_robots ]
do
	flagPos=0
	flagNext=0
	flagEquity=0
	while read line
	do
		let "flagPos+=1"
		if [ $flagPos -eq 2 ]
		then
			pos_robot[$robot]=`echo -n $line | sed -r -n 's/^[^0-9]*([0-9]+)\)$/\1/p'`
		fi
		if [ `echo -n $line | grep -E -c "^\(define-fun p$robot "` -eq 1 ]
		then
			flagPos=1
		else
			flagPos=0
		fi

		let "flagNext+=1"
		if [ $flagNext -eq 2 ]
		then
			next_move[$robot]=`echo -n $line | sed -r -n 's/^[^0-9\-]*([^)]+)\)+$/\1/p'`
			echo ${next_move[$robot]}
			echo `echo -n ${next_move[$robot]} | grep "- 1"`
			########### POURQUOI LE GREP NE FONCTIONNE PAS ??????????????????????????????????????????????????????????????
			# if [ `echo -n ${next_move[$robot]} | grep -E -c "- 1"` -eq 1 ]
			# then
			# 	echo oupsi
			# fi
		fi
		if [ `echo -n $line | grep -E -c "^\(define-fun s$robot "` -eq 1 ]
		then
			flagNext=1
		else
			flagNext=0
		fi

		let "flagEquity+=1"
		if [ $flagEquity -eq 2 ]
		then
			equity_bit[$robot]=`echo -n $line | sed -r -n 's/^[^0-9]*([0-9]+)\)$/\1/p'`
		fi
		if [ `echo -n $line | grep -E -c "^\(define-fun t$robot "` -eq 1 ]
		then
			flagEquity=1
		else
			flagEquity=0
		fi
	done < $file_log
	# flag=0
	# while read line
	# do
	# 	let "flag+=1"
	# 	if [ $flag -eq 2 ]
	# 	then
	# 		pos=`echo -n $line | sed -r -n 's/^[^0-9]*([0-9]+)\)$/\1/p'`
	# 		echo "robot $robot : position : $pos"
	# 		sed -r -i "s/(^p$pos :.*$)/\1 ($robot)/g" ./res.txt
	# 		break
	# 	fi
	# 	if [ `echo -n $line | grep -E -c "^\(define-fun p$robot "` -eq 1 ]
	# 	then
	# 		flag=1
	# 	else
	# 		flag=0
	# 	fi
	# done < $file_log

	# flag=0
	# while read line
	# do
	# 	let "flag+=1"
	# 	if [ $flag -eq 2 ]
	# 	then
	# 		stat=`echo -n $line | sed -r -n 's/^[^0-9\-]*([^)]+)\)+$/\1/p'`
	# 		echo "robot $robot : status : $stat"
	# 		sed -r -i "s/(^.* \($robot)(.*)$/\1, $stat\2/g" ./res.txt
	# 		break
	# 	fi
	# 	if [ `echo -n $line | grep -E -c "^\(define-fun s$robot "` -eq 1 ]
	# 	then
	# 		flag=1
	# 	else
	# 		flag=0
	# 	fi
	# done < $file_log

	# flag=0
	# while read line
	# do
	# 	let "flag+=1"
	# 	if [ $flag -eq 2 ]
	# 	then
	# 		bitT=`echo -n $line | sed -r -n 's/^[^0-9\-]*([^)]+)\)+$/\1/p'`
	# 		echo "robot $robot : bitT : $bitT"
	# 		sed -r -i "s/(^.* \($robot,[^)]+)(\).*$)/\1, $bitT\2/g" ./res.txt
	# 		break
	# 	fi
	# 	if [ `echo -n $line | grep -E -c "^\(define-fun t$robot "` -eq 1 ]
	# 	then
	# 		flag=1
	# 	else
	# 		flag=0
	# 	fi
	# done < $file_log
	let "robot+=1"
done
echo ${pos_robot[*]}
echo ${next_move[*]}
echo ${equity_bit[*]}
# loop=0
# while [ $loop -ne $size_loop ]
# do
# 	echo $loop
# 	let "loop+=1"
# done