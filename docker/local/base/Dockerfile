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

ENV PATH="/home/django/.local/bin:/home/django/.cargo/bin:${PATH}"

RUN useradd -m $USED_ID django \
    && echo "django:django" | chpasswd \
    && adduser django sudo \
    && chsh django -s /bin/bash

RUN chown -R django:django /home/django

RUN apt-get update && apt-get install -yy git gcc curl sudo

WORKDIR /app

RUN pip install poetry==1.0.5 maturin==0.8.1

USER django

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
    | sh -s -- -y --profile minimal --default-toolchain nightly
