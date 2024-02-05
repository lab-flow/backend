if not exist ".venv" CALL python -m venv .venv
CALL .venv\Scripts\activate.bat
CALL python.exe -m pip install --upgrade pip
CALL py -m pip install Django
CALL pip install "psycopg[binary]"
CALL pip install Pillow
CALL pip install djangorestframework
CALL pip install djangorestframework-simplejwt
CALL pip install django-cors-headers
CALL pip install pytest-django
CALL pip install django-extensions
CALL python -m pip install django-debug-toolbar
CALL pip install pylint-django
CALL py -m pip install reportlab
CALL pip install drf-standardized-errors
CALL pip install django-filter
CALL pip install python-dateutil
CALL pip install django-simple-history
PAUSE
