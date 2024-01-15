#!/bin/bash

yum install -y pip
yum install -y git
yum install -y tmux

cd /home/ec2-user
wget https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable-110.0.5481.177-1.x86_64.rpm
yum install -y google-chrome-stable-110.0.5481.177-1.x86_64.rpm

git clone https://github.com/kohjiahng/carousellscraper
chmod -R 777 carousellscraper
cd carousellscraper

echo "DISCORD_TOKEN=MTE5NDkyNDQ1Njc2MjY4NzUwOA.GLLFps.jTbgkJMQgJrtxBFOgLAsirjQR1nnJxKG29T4sI
LOG_FILE=logs.txt" > .env

# chrome can only be run as non-root user fsr

su ec2-user -c 'pip install --user -r requirements.txt'
tmux new -d "su ec2-user -c 'python3 bot.py'"