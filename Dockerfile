FROM python:3.9

LABEL Author="Kris Litman"
LABEL Application="Song Discovery"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /django_song_search

WORKDIR /django_song_search

RUN pip install poetry

COPY requirements.txt .

RUN poetry install -r requirements.txt

COPY ./django_song_search /django_song_search

CMD [ "poetry python manage.py runserver 0.0.0.0:8000" ]


