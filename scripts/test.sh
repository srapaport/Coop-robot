#! /bin/bash
for file in `ls`
do
    echo $file
    sed -r -i 's/^(Init \+ )phiSM$/\1phiR/g' $file
done