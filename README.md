# JolAdniJo - Django backend

Ez a https://joladnijo.jmsz.hu adományozási információkat segítő oldal backendjének repója.

[Projektünk](https://github.com/orgs/joladnijo/projects/1/) működéséről, az issue-k feldolgozásának módjáról, és a bekapcsolódási lehetőségekről lásd a [központi README](https://github.com/joladnijo/joladnijo-docs/blob/main/README.md#hogyan-seg%C3%ADthetsz---m%C5%B1k%C3%B6d%C3%A9s%C3%BCnk)-t.

## Requirements

* python 3.9 (was created using `3.9.10`)
* django 3.2
* mySQL 5.7

## Setup development environment

### Virtualenv

Create and activate virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

### Environment variables

| Name | Description | Example |
| --- | --- | --- |
| DBPASSWORD | Password for MySQL DB | secure-password
| DBHOST | DB host (optional, defaults to `localhost`) | 127.0.0.1
| DBPORT | DB server port (optional, defaults to `3306`) | 3306
| SECRET_KEY | Django secret key | very-secret-key
| JWT_AUDIENCE |  Expected audience for JWT tokens | https://joladnijo.jmsz.hu/api/
| JWT_KEYS | Full URL to `jwks.json` keys file | https://dev-ulmlyx6h.eu.auth0.com/.well-known/jwks.json
| JWT_ISSUER | Expected JWT token issuer | https://dev-ulmlyx6h.eu.auth0.com/
| JWT_ALGORITHM | Signing algorithm for JWT tokens, defaults to `RS256` | 

### MySQL

Create user `'svc_backend'@'localhost'`, database `joladnijo` and grant all privileges on the database to the user:

```sql
CREATE USER 'svc_backend'@'localhost';
CREATE DATABASE joladnijo;
GRANT ALL PRIVILEGES ON `joladnijo`.* TO 'svc_backend'@'localhost';
```

### Migration

In the project folder issue the `migrate` command (with your venv activated)

```bash
./manage.py migrate
```

### Start dev server

```bash
./manage.py runserver
```

### Start docker compose stack with MySQL database (dev mode)
```bash
docker-compose up --build
```

### Start docker compose stack with MySQL database (production mode)
```bash
docker-compose -f docker-compose.prod.yml up --build
```
