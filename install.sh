#!/bin/bash

apt update -y
apt install python3 python3-pip -y

pip3 install -r requirements.txt

echo "Bot starting..."
python3 bot.py
