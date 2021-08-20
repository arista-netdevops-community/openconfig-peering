#!/bin/bash
rm -Rf venv/ bgpq4/ json/
mkdir json/
virtualenv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install pyang pyangbind requests
PWD=`pwd`
for i in `ls $PWD/venv/lib`; do ln -s $PWD/venv/lib/$i $PWD/venv/lib/python3 ; done
git clone https://github.com/bgp/bgpq4.git
cd bgpq4
./bootstrap
./configure
make
cd ..