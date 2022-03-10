FROM python:3.9

COPY requirements.txt ./
RUN apt-get update \
    && apt-get install python3-dev -y \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

WORKDIR /code
ENV PYTHONPATH /code:$PYTHONPATH
EXPOSE 8000

CMD python manage.py runserver