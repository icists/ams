DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd ../ && pwd )
docker run -d -i -v $DIR:/ams -t -p 80:80 ams /bin/bash -c "service mysql start; python /ams/ams_base/manage.py runserver 0.0.0.0:80"
