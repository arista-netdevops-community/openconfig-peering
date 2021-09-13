#!/bin/bash
if ! command -v go &> /dev/null
then
    echo "go could not be found - please install go"
    exit
fi

export `go env | grep GOPATH | sed 's/\"//g'`

rm -Rf venv/ tools/ json/ $GOPATH/src/github.com/openconfig/
mkdir json/
mkdir tools/

#pyang and virtualenv
virtualenv venv
source venv/bin/activate
pip3 install --upgrade pip
pip3 install pyang pyangbind requests
PWD=`pwd`
for i in `ls $PWD/venv/lib`; do ln -s $PWD/venv/lib/$i $PWD/venv/lib/python3 ; done

# gnmic
cd tools
git clone https://github.com/karimra/gnmic.git
cd gnmic
go get
go build
cd ../../

# gnoic
cd tools
git clone https://github.com/karimra/gnoic.git
cd gnoic
go get
go build
cd ../../

# grpcurl
cd tools
mkdir -p $GOPATH/src/github.com/openconfig
git clone https://github.com/openconfig/gnoi.git $GOPATH/src/github.com/openconfig/gnoi
git clone https://github.com/fullstorydev/grpcurl.git
cd grpcurl
go get github.com/openconfig/gnoi
go get
go build
cd cmd/grpcurl/
go get
go build
cd ../../
cd ../../

# bgpq4
cd tools
git clone https://github.com/bgp/bgpq4.git
cd bgpq4
./bootstrap
./configure
make
cd ../../