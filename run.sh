#! /bin/bash


# first run
# get ams_base/icists/mysql.cnf
# get ams_base/secret.key
# create database application_icists

# dump application_icists database
# mysqldump -u [user] -p application_icists > filename.sql
# mysql -u [user] -p application_icists < filename.sql



source env/bin/activate
python ams_base/manage.py runserver --insecure 0.0.0.0:21034
