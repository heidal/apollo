#!/bin/bash

set -e

if [[ "$PWD" = "/app" ]]; then

COMPOSE=""

else

COMPOSE="docker-compose exec app"

fi

$COMPOSE python manage.py makemigrations --check
$COMPOSE black --check .
$COMPOSE mypy apollo
$COMPOSE pytest
