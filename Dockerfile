FROM python:3.12-slim

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./req.txt /usr/src/app/

RUN pip install -r requirements.txt

COPY . /usr/src/app/