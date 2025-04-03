#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles
mkdir -p media

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create cache table for database cache backend
echo "Creating cache table..."
python manage.py createcachetable

# Create symbolic link from media to staticfiles for WhiteNoise
echo "Setting up media files for production..."
if [ -d "media" ] && [ -d "staticfiles" ]; then
    cp -r media/* staticfiles/ 2>/dev/null || true
    echo "Media files copied to staticfiles directory"
fi

echo "Build completed successfully!"
