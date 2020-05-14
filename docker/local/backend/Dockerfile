FROM docker.pkg.github.com/apollo/apollo-base:latest

EXPOSE 8000

COPY ./backend/poetry.lock ./backend/pyproject.toml /app/

COPY --chown=django:django ./apollo-crypto/apollo-crypto-python /apollo-crypto-python
COPY --chown=django:django ./apollo-crypto/apollo-crypto-core /apollo-crypto-core

RUN poetry config virtualenvs.create false

USER root
RUN poetry install

USER django

RUN pip install /apollo-crypto-python

COPY ./docker/local/backend/entrypoint.sh /entrypoint.sh
COPY ./docker/local/backend/start.sh /start.sh

COPY --chown=django:django ./backend /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
