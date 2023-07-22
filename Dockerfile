FROM python:3.10

ENV PIP_NO_CACHE_DIR off

ENV PIP_DISABLE_PIP_VERSION_CHECK on

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

ENV COLUMNS 80

WORKDIR /app

COPY requirements/dev.txt /app/requirements/dev.txt

RUN apt-get update -y \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && pip install -r requirements/dev.txt \
    && apt-get install -y gdal-bin libgdal-dev

COPY . /app