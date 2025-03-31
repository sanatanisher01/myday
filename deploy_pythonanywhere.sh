#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Migrate database
python manage.py migrate

# Run tests (optional)
python manage.py test

# Restart the application
pythonanywhere restart
