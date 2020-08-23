#!/bin/bash
# Installer for X-Board Configurator and Service
# Installatoin of required libraries
sudo apt-get update --fix-missing
sudo apt upgrade
sudo apt install git
sudo apt-get install libmodbus-dev
sudo apt-get install sqlite3
sudo apt-get install libsqlite3-dev
sudo apt-get install sqlitebrowser
sudo apt install mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
sudo apt-get install libbson-1.0
sudo apt-get install libmongoc-1.0-0
sudo apt install python3-virtualenv

# Installatoin of virtual environment
cd ~
mkdir python3_virtualenv
cd python3_virtualenv/
virtualenv -p /usr/bin/python3 commservice_env
pip install -r requirements.txt

# Create Comm Service at boot up
chmod u+x ~/installer/commservice.sh
sudo cp ~/installer/commservice.service /etc/systemd/system/commservice.service
sudo systemctl start commservice
sudo systemctl enable commservice