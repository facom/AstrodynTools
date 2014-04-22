#!/bin/bash
DIR=$(pwd)

########################################
#INSTALL GSL
########################################
echo "Installing GSL..."
if [ ! -e util/lib/libgsl.a ];then
    cd util
    tar zxf gsl.tar.gz
    cd gsl
    ./configure --prefix=$DIR/util && make && make install
    cd ..
    rm -rf gsl
    echo "Done."
else
    echo "Already installed."
fi
cd $DIR

########################################
#INSTALL CSPICE
########################################
echo "Installing SPICE..."
if [ ! -e util/lib/cspice.a ];then
    cd util
    tar Zxf cspice.tar.Z
    cd cspice
    ./makeall.csh
    mv include/* ../include
    mv lib/* ../lib
    cd ..
    rm -rf cspice
    echo "Done."
else
    echo "Already installed."
fi
cd $DIR

########################################
#DOWNLOAD MERCUPY
########################################
echo "Installing MercuPy..."
if [ ! -d MercuPy ];then
    if [ $1 = "admin" ];then
	echo "Getting contributor copy..."
	git clone git@github.com:facom/MercuPy.git
    else
	echo "Getting user copy..."
	git clone http://github.com/facom/MercuPy.git
    fi
    cd MercuPy
    CSPICE=$DIR/util/lib make utilbuild
    echo "Done."
else
    echo "Already installed."
fi
cd $DIR

########################################
#INSTALL PYTHON NOVAS
########################################
echo "Installing Python Novas..."
if [ ! -d util/lib/python2.7 ];then
    cd util
    tar zxf novas.tgz
    cd novas
    CC=gcc python setup.py build install --prefix=$DIR/util
    cd ..
    rm -rf novas
    echo "Done."
else
    echo "Already installed."
fi
cd $DIR

########################################
#INSTALL PYTHON NOVAS
########################################
echo "Installing C Novas..."
if [ ! -d util/lib/novas.a ];then
    cd util
    tar zxf novasc.tgz
    cd novasc
    make install
    cd ..
    rm -rf novasc
    echo "Done."
else
    echo "Already installed."
fi
cd $DIR

echo "Setting python path..."
cmd="export PYTHONPATH=\$PYTHONPATH:util/lib/python2.7/site-packages"
echo "Set path as: $cmd"
echo $cmd > /tmp/path
source /tmp/path
