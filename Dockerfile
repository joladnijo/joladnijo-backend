FROM python:3.9-slim as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH="${PATH}:/root/.poetry/bin"

RUN apt-get update \
    && apt-get install curl gcc default-libmysqlclient-dev python3-dev binutils libproj-dev gdal-bin -y
RUN which curl

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-root

ENV PYTHONPATH /app:$PYTHONPATH

EXPOSE 8000

COPY . /app/
CMD ./start-django.sh
