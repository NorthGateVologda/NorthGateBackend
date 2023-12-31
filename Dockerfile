FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN apt-get update -y \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && pip install -r requirements/dev.txt \
    && apt-get install -y gdal-bin libgdal-dev