#! /bin/bash
if [ $# == 0 ]
then
	echo "usage : ./patchModelRef.sh <python version> <reverse>"
	exit 0
fi
if [ $# > 1 ]
then
	sudo patch --reverse -d /usr/lib/python$1/site-packages/z3/ < /usr/lib/python$1/site-packages/z3/ajoutException.patch
	exit 0
fi
sudo patch -d /usr/lib/python$1/site-packages/z3/ < /usr/lib/python$1/site-packages/z3/ajoutException.patch
exit 0
