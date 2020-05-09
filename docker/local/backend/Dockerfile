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

RUN apt-get update && apt-get install -yy git gcc
RUN pip install poetry==1.0.5

RUN mkdir /app
WORKDIR /app

COPY ./backend/poetry.lock ./backend/pyproject.toml /app/

RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./docker/local/backend/entrypoint.sh /entrypoint.sh
COPY ./docker/local/backend/start.sh /start.sh

RUN useradd -u 1000 django
USER django

COPY --chown=django:django ./backend /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
