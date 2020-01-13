FROM python:3.8.1-slim

ARG USER_ID=1000
ENV HOME=/home/django

RUN apt-get update && apt-get -yy install build-essential

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./backend /app
WORKDIR /app

RUN poetry update && poetry install

COPY ./docker/local/backend/entrypoint.sh /entrypoint.sh
COPY ./docker/local/backend/start.sh /start.sh

RUN useradd --create-home --uid $USER_ID django

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
