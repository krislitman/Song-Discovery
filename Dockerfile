FROM python:3.8

LABEL Author="Kris Litman"
LABEL Application="Song Discovery"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /django_song_search
WORKDIR /django_song_search

RUN pip install pipenv && pipenv install --upgrade pipenv

COPY requirements.txt .

RUN pipenv install -r requirements.txt

COPY ./django_song_search /django_song_search

CMD [ "python manage.py runserver 0.0.0.0:8000" ]


