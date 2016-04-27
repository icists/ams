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

At the project directory, run:
```sh
$ virtualenv env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```

# To import MySQL sql file #
Log in to MySQL and create a database named 'application_icists'
mysql -u [mysql_username] -p application_icists < [imported_sql_file]

# To run the program #
```sh
(env)$ python manage.py runserver 0.0.0.0:[port]
```

or to run on port 80 as sudo:
(env)$ sudo ../env/bin/python manage.py runserver 0.0.0.0:80
