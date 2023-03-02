#!/bin/bash

# author: greyshell
# description: install python3.7

apt install build-essential
# apt install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt update
apt install -y python3.7
# pip3.7 install -r requrements.txt