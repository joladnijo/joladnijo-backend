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

### MySQL

Create user `'joladnijo'@'localhost'`, database `joladnijo` and grant all privileges on the database to the user:

```sql
CREATE USER 'joladnijo'@'localhost';
CREATE DATABASE joladnijo;
GRANT ALL PRIVILEGES ON `joladnijo`.* TO 'joladnijo'@'localhost';
```
