docker run -i -v -d ../:/ams -t -p 127.0.0.1:80:80 ams /bin/bash -c "service mysql start; python /ams/ams_base/manage.py runserver 0.0.0.0:80"
