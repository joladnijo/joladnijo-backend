# JolAdniJo - Django backend

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

| Name | Example |
| --- | --- |
| DBENGINE | django.db.backends.mysql
| DBNAME | joladnijo
| DBUSER | joladnijo
| DBPASSWORD | secure-password
| DBHOST | 127.0.0.1
| DBPORT | 3306
| SECRET_KEY | very-secret-key

### MySQL

Create user `'joladnijo'@'localhost'`, database `joladnijo` and grant all privileges on the database to the user:

```sql
CREATE USER 'joladnijo'@'localhost';
CREATE DATABASE joladnijo;
GRANT ALL PRIVILEGES ON `joladnijo`.* TO 'joladnijo'@'localhost';
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