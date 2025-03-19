#!/bin/bash

apt install  build-essential libreadline-dev zlib1g-dev libbz2-dev liblzma-dev libpcre2-dev gfortran libcurl4-openssl-dev default-jdk texlive-latex-base cmake libxml2-dev texinfo libpng-dev 
cd /opt
wget https://cran.r-project.org/src/base/R-4/R-4.3.1.tar.gz
tar -xzvf R-4.3.1.tar.gz
cd R-4.3.1
./configure --with-x=no --with-png --enable-R-shlib
make
make install
cd /opt
rm R-4.3.1.tar.gz
