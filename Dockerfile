# Build stage 1: Acquire packages
FROM python:3.9-alpine as base

ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt ./
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev binutils libproj-dev gdal-bin \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' +

# Build stage 2: copy packages & binaries & source code to final slim image
FROM python:3.9-alpine

COPY --from=base /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/

RUN apk update && apk add --no-cache mariadb-dev binutils libproj-dev gdal-bin

WORKDIR /code

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /code:$PYTHONPATH
EXPOSE 8000

COPY . /code/
CMD python manage.py migrate && python manage.py runserver