FROM python:3.10

ENV PIP_NO_CACHE_DIR off \
    PIP_DISABLE_PIP_VERSION_CHECK on \
    PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1 \
    COLUMNS 80

WORKDIR /app

COPY . /app

RUN apt-get update -y \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && pip install -r requirements/dev.txt \
    && apt-get install -y gdal-bin libgdal-dev