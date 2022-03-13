runserver:
	docker-compose up -d mysql
	DBPASSWORD=testsvcpassword SECRET_KEY=verysecretkey APP_DEBUG=True ./manage.py runserver