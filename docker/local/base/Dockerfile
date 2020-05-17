FROM python:3.8-slim-buster

EXPOSE 8000

ARG USER_ID=1000
ENV HOME=/home/django \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.0.0

RUN useradd -m $USED_ID django

RUN chown -R django:django /home/django

RUN apt-get update && apt-get install -yy git gcc

WORKDIR /app

RUN pip install poetry==1.0.5

USER root

COPY ./backend/poetry.lock ./backend/pyproject.toml /app/
RUN poetry config virtualenvs.create false
RUN poetry install
