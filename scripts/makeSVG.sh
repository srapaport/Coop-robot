#§ /bin/bash
for file in `ls ../rapport/`
do
    if [ `echo $file | grep -c -E '^.*\.svg$'` == 1 ]
    then
        inkscape -D -z --file=$file --export-pdf=`echo $file | sed -r -n 's/^(.*)\.svg$/\1/p'`.pdf --export-latex
    fi
done