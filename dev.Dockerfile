FROM python:3.9

ENV PYTHONPATH /app:$PYTHONPATH
ENV PYTHONUNBUFFERED 1
ENV PATH="${PATH}:/root/.poetry/bin"

RUN apt-get update \
    && apt-get install python3-dev binutils libproj-dev gdal-bin -y

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN poetry config virtualenvs.create false

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-root

EXPOSE 8000

CMD ./start-django.sh
