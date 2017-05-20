FROM ubuntu:latest

RUN apt-get -y update \
	&& apt-get install -y apt-utils \                                           
    	&& { \
	echo debconf debconf/frontend select Noninteractive; \
        echo mysql-community-server mysql-community-server/data-dir \
            select ''; \
        echo mysql-community-server mysql-community-server/root-pass \
            password 'JohnUskglass'; \
        echo mysql-community-server mysql-community-server/re-root-pass \
            password 'JohnUskglass'; \
        echo mysql-community-server mysql-community-server/remove-test-db \
            select true; \
    	} | debconf-set-selections \
	&& apt-get install -y git python-dev mysql-server libmysqlclient-dev python-virtualenv gcc curl

RUN curl -O https://bootstrap.pypa.io/get-pip.py && python get-pip.py
WORKDIR /ams
COPY deployment/requirements.txt .
COPY deployment/skeleton.sql .
RUN pip install --requirement requirements.txt
RUN service mysql start && mysql -u root --execute='CREATE DATABASE application_icists' \
	&& mysql -u root application_icists < deployment/skeleton.sql

EXPOSE 80
VOLUME ["/ams"]

