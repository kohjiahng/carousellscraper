#!/bin/sh

sudo yum install pip
sudo yum install git
sudo yum install tmux
pip install pipenv

git clone https://github.com/kohjiahng/carousellscraper

cd carousellscraper

git pull origin master

pipenv --python /usr/bin/python3
pipenv install


echo "DISCORD_TOKEN={TOKEN}
LOG_FILE=logs.txt" > .env

sudo wget https://dl.google.com/linux/chrome/rpm/stable/x86_64/google-chrome-stable-110.0.5481.177-1.x86_64.rpm && yum localinstall -y google-chrome-stable-110.0.5481.177-1.x86_64.rpm


tmux new -d 'pipenv run python3 bot.py'