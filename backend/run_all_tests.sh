#!/bin/bash

set -e

docker-compose exec app python manage.py makemigrations --check
docker-compose exec app black --check .
docker-compose exec app mypy apollo
docker-compose exec app python manage.py test --settings config.settings.test
