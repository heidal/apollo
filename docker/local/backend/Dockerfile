FROM apollo-base

USER django

COPY ./docker/local/backend/entrypoint.sh /entrypoint.sh
COPY ./docker/local/backend/start.sh /start.sh

COPY --chown=django:django ./backend /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
