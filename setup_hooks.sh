#!/usr/bin/env bash

echo "******************************installing hooks***********************************************"
cd ./.git/
rm -rf hooks
ln -s ../hooks
echo "***************************installation successful*******************************************"
