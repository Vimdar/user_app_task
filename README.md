# A simple API for a task, that supports CRUD of users

## Start
- create a virtualenv with python3.12.*
- run ```pip install requirements.txt```
- make sure you have a .env file with all the variables needed; example one looks like:
```
#API
DEBUG=True
PRODUCTION=False
DBNAME=...
DBUSER=...
DBPASS=...
DBHOST=localhost
DBPORT=...
DBSCHEMA=...
DBENGINE=django.db.backends.postgresql_psycopg2
SECRET_KEY=...
POSTGRES_USER=...
POSTGRES_PASSWORD=...
OPENAI_API_KEY=...
AI_PROFILE_PICTURES_GENERATION_ENABLED=False
# docker-compose-dev
DBPORT_OUT=...
DBPORT_IN=...
```
- make sure you got postgresql running locally and env vars reflect your setup OR
- use docker-compose-dev.yml to create a persistant DB container to use (env vars should reflect your setup as well)
- docker-compose-dev.yml is for dev purposes only
- All the latter commands are shown as run from repo root
- run ```./manage.py makemigrations && ./manage.py migrate```
- for a dev server run ```./manage.py runserver```

## Tests:
- to run tests execute python ```pytest apps/ (-s for debug)```
- mypy with ```mypy . ```
- pylint with ```pylint .```
