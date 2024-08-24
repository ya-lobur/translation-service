FROM python:3.11.8-bullseye
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN apt update && pip3 install poetry

WORKDIR /translation-service

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

COPY . /translation-service

EXPOSE 8000
