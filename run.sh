#! /bin/bash
source env/bin/activate
python ams_base/manage.py runserver --insecure 0.0.0.0:21034
