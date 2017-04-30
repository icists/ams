FROM ubuntu:latest

RUN apt-get -y update && apt-get install -y git python-dev mysql-server libmysqlclient-dev python-virtualenv gcc

RUN virtualenv env
RUN source env/bin/activate
RUN pip install -r requirements.txt
RUN service mysql start

