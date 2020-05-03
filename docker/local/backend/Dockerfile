FROM python:3.8-alpine

EXPOSE 8000

ARG USER_ID=1000
ENV HOME=/home/django

RUN apk add build-base libffi-dev openssl-dev git postgresql-dev bash

RUN mkdir /app
WORKDIR /app

COPY ./backend/requirements-dev.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./docker/local/backend/entrypoint.sh /entrypoint.sh
COPY ./docker/local/backend/start.sh /start.sh

RUN addgroup -S django && adduser -S django -G django
USER django

COPY --chown=django:django ./backend /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
