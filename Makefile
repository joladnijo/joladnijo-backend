runserver:
	docker-compose up -d mysql
	DBPASSWORD=testsvcpassword \
	SECRET_KEY=verysecretkey  \
	APP_DEBUG=True \
	JWT_AUDIENCE='https://joladnijo.jmsz.hu/api/' \
	JWT_ISSUER='https://dev-ulmlyx6h.eu.auth0.com/' \
	JWT_KEYS='https://dev-ulmlyx6h.eu.auth0.com/.well-known/jwks.json' \
	./start-django.sh

docker-compose-prod:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build

docker-compose-prod-down:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml down

schema:
	python manage.py generateschema --format openapi-json --file openapi-schema.json

install:
	pip install -r requirements.txt

format:
	isort joladnijo/
	black -l 120 joladnijo/ --skip-string-normalization

flake:
	flake8 joladnijo/ --ignore=E203,W503

black:
	black -l 120 --check joladnijo/ --skip-string-normalization

typing:
	mypy --show-error-codes -p joladnijo

lint: black flake typing

unit:
	echo "todo"

test: lint unit
