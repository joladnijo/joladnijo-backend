#!/bin/sh

python manage.py check_db
python manage.py migrate

if [ "$ENVIRONMENT" = 'development' ] || [ "$ENVIRONMENT" = 'staging' ]
then
    python manage.py loaddata seeds/default.yaml
	python manage.py loaddata seeds/sample.yaml
    python manage.py createsuperuser --no-input
fi

python manage.py runserver 0.0.0.0:8000