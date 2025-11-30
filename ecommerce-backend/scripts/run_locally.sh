#!/usr/bin/env bash
set -e
export $(grep -v '^#' ../.env | xargs)
python manage.py migrate
python manage.py loaddata || true
python manage.py seed || true
python manage.py runserver 0.0.0.0:8000
