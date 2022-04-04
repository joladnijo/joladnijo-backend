#!/bin/sh

python manage.py check_db
python manage.py migrate

if [ "$ENVIRONMENT" = 'development' ] || [ "$ENVIRONMENT" = 'staging' ]
then
    python manage.py loaddata seeds/default.yaml
fi

python manage.py runserver 0.0.0.0:8000