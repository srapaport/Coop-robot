#! /bin/bash
sudo patch $1 -d /usr/lib/python3.8/site-packages/z3/ < /usr/lib/python3.8/site-packages/z3/ajoutException.patch
