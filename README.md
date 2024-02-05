# Hazardous Reagents backend
This repo contains code for the backend written in Django and PostgreSQL.

## Requirements
- Python 3.9.16
- PostgreSQL 15.4

Python 3.12.1 with Django 5.0 was also tested in a dev/test environment but not in production.

## Configuration
1. Create a virtual environment (e.g. `venv`). Activate it and upgrade `pip` with `pip install --upgrade pip`.
2. Install all required dependencies with `pip install -r requirements.txt`. Alternatively, use the script [for Linux](setup.sh) or [for Windows](setup.bat) which will install the latest available packages.
3. Add every required environmental variable, that is:
    - from the [settings file](backend/backend/settings.py):
        - `SECRET_KEY`: the secret key required by Django (more details [here](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/#secret-key))
        - `PG_NAME`, `PG_USER`, `PG_PASSWORD`, `PG_HOST`, `PG_PORT`: the database settings (more details [here](https://docs.djangoproject.com/en/stable/ref/settings/#databases))
    - from the [generators module](backend/reagents/generators.py); they indicate paths to .ttf files with specified font types:
        - `REGULAR_FONT`
        - `BOLD_FONT`
        - `ITALIC_FONT`
4. Create a PostgreSQL database.
5. Run `python manage.py migrate` to create tables and relations in the database.

## Dev/test environment
1. Set the `DEBUG` variable in the [settings file](backend/backend/settings.py) to `True`.
2. In the [settings file](backend/backend/settings.py) add appropriate IP addresses to `CORS_ALLOWED_ORIGINS` (more details [here](https://github.com/adamchainz/django-cors-headers#cors_allowed_origins-sequencestr)).
3. Run a dev/test server: `python manage.py runserver`

## Deployment
1. Pick an HTTP server (e.g. [httpd with mod_wsgi](https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/modwsgi/)). It will be used to serve both the app and the media ([Django doesn't do that by itself](https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/modwsgi/#serving-files)).
2. In the [settings file](backend/backend/settings.py) add appropriate IP addresses to `CORS_ALLOWED_ORIGINS` (more details [here](https://github.com/adamchainz/django-cors-headers#cors_allowed_origins-sequencestr)).
3. Go through the [deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/).
4. Deploy the app to the web server.

## Running tests
Run `python runtests.py`.

## Some useful commands
- Create an admin user: `python manage.py createsuperuser`
- Clean duplicate history records: `python manage.py clean_duplicate_history --auto`
- Make a migration: `python manage.py makemigrations reagents`
- Show available URLs: `python manage.py show_urls`
