#!/bin/bash

if [ ! -d ".venv" ]
then
python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
python -m pip install Django
pip install "psycopg[binary]"
pip install Pillow
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install pytest-django
pip install django-extensions
python -m pip install django-debug-toolbar
pip install pylint-django
python -m pip install reportlab
pip install drf-standardized-errors
pip install django-filter
pip install setuptools
pip install python-dateutil
pip install django-simple-history
