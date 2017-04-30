ICISTS-KAIST 2015 Registration
==============================

# Requirements for installation #
There are a few packages that need to be installed before running this django application. 

* python
* mysql-server
* libmysqlclient-dev

In Ubuntu, these can be installed by the following command:

```sh
$ sudo apt-get install [package-name]
```

At the project directory, run install.sh, which contains the following commands:
```sh
$ virtualenv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```

# To import MySQL sql file #
Log in to MySQL and create a database named 'application_icists'
```sh
mysql -u [mysql_username] -p application_icists < [imported_sql_file]
```

# To run the program #
```sh
(env)$ python manage.py runserver 0.0.0.0:[port]
```

or to run on port 80 as sudo:
```sh
(env)$ sudo ../env/bin/python manage.py runserver 0.0.0.0:80
```

or instead, use the `run.sh`, script which contains the above command.




# How to run with Docker #

## run Dockerfile ##


## 

```sh
docker run -i -v /ams:/Users/zoonoo/repo/ams -t ubuntu
```
