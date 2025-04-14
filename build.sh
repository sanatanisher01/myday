#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles

# Check if we're on Render (persistent disk is mounted at /opt/render/project/src/media)
if [ -d "/opt/render/project/src" ]; then
    echo "Running on Render with persistent disk..."
    # Ensure the media directory exists on the persistent disk
    mkdir -p /opt/render/project/src/media
    mkdir -p /opt/render/project/src/media/events
    mkdir -p /opt/render/project/src/media/subevents
    mkdir -p /opt/render/project/src/media/reviews
    mkdir -p /opt/render/project/src/media/avatars
    mkdir -p /opt/render/project/src/media/gallery
    mkdir -p /opt/render/project/src/media/categories

    # Set proper permissions
    chmod -R 755 /opt/render/project/src/media

    # Instead of creating a symbolic link which can cause recursive issues,
    # we'll just use the persistent disk path directly in settings.py
else
    echo "Running locally..."
    # Create local media directories
    mkdir -p media
    mkdir -p media/events
    mkdir -p media/subevents
    mkdir -p media/reviews
    mkdir -p media/avatars
    mkdir -p media/gallery
    mkdir -p media/categories
fi

# Create sample event images if they don't exist
echo "Setting up default event images..."
cp -r static/images/event-placeholder.jpg media/events/default-wedding.jpg 2>/dev/null || true
cp -r static/images/event-placeholder.jpg media/events/default-birthday.jpg 2>/dev/null || true
cp -r static/images/event-placeholder.jpg media/events/default-anniversary.jpg 2>/dev/null || true
cp -r static/images/event-placeholder.jpg media/events/default-corporate.jpg 2>/dev/null || true

# Make the image persistence script executable
chmod +x ensure_image_persistence.py

# Collect static files
echo "Collecting static files..."
DJANGO_SETTINGS_MODULE=myday.settings python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Apply specific migration for image field length
echo "Applying image field migration..."
python manage.py migrate events 0011_increase_image_field_length

# Create cache table for database cache backend
echo "Creating cache table..."
python manage.py createcachetable

# Run the image persistence script to ensure all images are in the persistent storage
echo "Ensuring image persistence..."
python ensure_image_persistence.py

# Copy media files to staticfiles for WhiteNoise to serve them
echo "Setting up media files for production..."
if [ -d "media" ] && [ -d "staticfiles" ]; then
    # Create media directory in staticfiles
    mkdir -p staticfiles/media

    # Copy all media files to staticfiles/media directory
    cp -r media/* staticfiles/media/ 2>/dev/null || true
    echo "Media files copied to staticfiles/media directory"

    # Also copy directly to staticfiles for backward compatibility
    cp -r media/* staticfiles/ 2>/dev/null || true
    echo "Media files copied to staticfiles directory"

    # Create a special events directory in staticfiles
    mkdir -p staticfiles/events
    cp -r media/events/* staticfiles/events/ 2>/dev/null || true
    echo "Event images copied to staticfiles/events directory"

    # Set proper permissions
    chmod -R 755 staticfiles/media staticfiles/events
fi

# Run a script to ensure default events exist
echo "Checking for default events..."
python manage.py shell -c """
try:
    from events.models import Event
    from django.core.files.base import ContentFile
    import os

    # Create default events if they don't exist
    default_events = [
        {'name': 'Wedding', 'slug': 'wedding', 'description': 'Beautiful wedding events and photography services.', 'image_path': 'media/events/default-wedding.jpg'},
        {'name': 'Birthday', 'slug': 'birthday', 'description': 'Memorable birthday celebration services.', 'image_path': 'media/events/default-birthday.jpg'},
        {'name': 'Anniversary', 'slug': 'anniversary', 'description': 'Special anniversary celebration services.', 'image_path': 'media/events/default-anniversary.jpg'},
        {'name': 'Corporate', 'slug': 'corporate', 'description': 'Professional corporate event services.', 'image_path': 'media/events/default-corporate.jpg'},
    ]

    for event_data in default_events:
        # Make sure slug is defined for each event
        slug = event_data['slug']
        event, created = Event.objects.get_or_create(
            slug=slug,
            defaults={
                'name': event_data['name'],
                'description': event_data['description']
            }
        )

        # Add default image if event has no image
        if created or not event.image:
            image_path = event_data['image_path']
            if os.path.exists(image_path):
                with open(image_path, 'rb') as f:
                    event.image.save(f'default-{slug}.jpg', ContentFile(f.read()))
                print(f'Added default image to {event.name} event')
            else:
                print(f'Warning: Default image not found at {image_path}')

    print(f'Checked default events. Total events: {Event.objects.count()}')
except Exception as e:
    print(f'Error checking default events: {str(e)}')
"""

echo "Build completed successfully!"
