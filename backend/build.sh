#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py loaddata books/fixtures/books.json
