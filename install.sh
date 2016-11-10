#! /bin/bash

# sudo apt-get install python-dev
# sudo apt-get install mysql-server
# sudo apt-get install libmysqlclient-dev
# sudo apt-get install python-virtualenv



virtualenv env
source env/bin/activate
pip install -r requirements.txt

# mysql dump
