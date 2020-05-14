FROM votifica/apollo-base:latest

USER django

COPY --chown=django:django ./apollo-crypto/apollo-crypto-python /apollo-crypto-python
COPY --chown=django:django ./apollo-crypto/apollo-crypto-core /apollo-crypto-core

RUN pip install /apollo-crypto-python

COPY ./docker/local/backend/entrypoint.sh /entrypoint.sh
COPY ./docker/local/backend/start.sh /start.sh

COPY --chown=django:django ./backend /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
