#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
python manage.py collectstatic --noinput

# Apply database migrations
python manage.py migrate
