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
| DBPASSWORD | secure-password
| DBHOST (optional, defaults to `localhost`) | 127.0.0.1
| DBPORT (optional, defaults to `3306`) | 3306
| SECRET_KEY | very-secret-key

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