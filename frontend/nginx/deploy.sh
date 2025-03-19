#!/bin/bash

openssl req -x509 -sha256 -nodes -newkey rsa:2048 -keyout ser.key -out ser.pem
cp -r ../dist .
cp ../.env dist/.env 

docker build . -t nginx-vue
docker run --rm -it -p 443:443 -p 80:80 nginx-vue
