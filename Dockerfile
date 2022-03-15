# Build stage 1: Acquire packages
FROM python:3.9-slim as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt ./
RUN apt-get update \
    && apt-get install gcc default-libmysqlclient-dev python3-dev binutils libproj-dev gdal-bin -y \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

WORKDIR /code
ENV PYTHONPATH /code:$PYTHONPATH
EXPOSE 8000

COPY . /code/
CMD ./start-django.sh
