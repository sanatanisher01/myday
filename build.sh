#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p staticfiles
mkdir -p media
mkdir -p media/events
mkdir -p media/subevents
mkdir -p media/reviews
mkdir -p media/avatars
mkdir -p media/gallery
mkdir -p media/categories

# Create sample event images if they don't exist
echo "Setting up default event images..."
cp -r static/images/event-placeholder.jpg media/events/default-wedding.jpg 2>/dev/null || true
cp -r static/images/event-placeholder.jpg media/events/default-birthday.jpg 2>/dev/null || true
cp -r static/images/event-placeholder.jpg media/events/default-anniversary.jpg 2>/dev/null || true
cp -r static/images/event-placeholder.jpg media/events/default-corporate.jpg 2>/dev/null || true

# Collect static files
echo "Collecting static files..."
DJANGO_SETTINGS_MODULE=myday.settings python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create cache table for database cache backend
echo "Creating cache table..."
python manage.py createcachetable

# Create symbolic link from media to staticfiles for WhiteNoise
echo "Setting up media files for production..."
if [ -d "media" ] && [ -d "staticfiles" ]; then
    # Copy all media files to staticfiles directory
    cp -r media/* staticfiles/ 2>/dev/null || true
    echo "Media files copied to staticfiles directory"
    
    # Create a special events directory in staticfiles
    mkdir -p staticfiles/events
    cp -r media/events/* staticfiles/events/ 2>/dev/null || true
    echo "Event images copied to staticfiles/events directory"
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
        {'name': 'Wedding', 'event_slug': 'wedding', 'description': 'Beautiful wedding events and photography services.', 'image_path': 'media/events/default-wedding.jpg'},
        {'name': 'Birthday', 'event_slug': 'birthday', 'description': 'Memorable birthday celebration services.', 'image_path': 'media/events/default-birthday.jpg'},
        {'name': 'Anniversary', 'event_slug': 'anniversary', 'description': 'Special anniversary celebration services.', 'image_path': 'media/events/default-anniversary.jpg'},
        {'name': 'Corporate', 'event_slug': 'corporate', 'description': 'Professional corporate event services.', 'image_path': 'media/events/default-corporate.jpg'},
    ]
    
    for event_data in default_events:
        event, created = Event.objects.get_or_create(
            event_slug=event_data['event_slug'],
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
                    event.image.save(f'default-{event_data["event_slug"]}.jpg', ContentFile(f.read()))
                print(f'Added default image to {event.name} event')
            else:
                print(f'Warning: Default image not found at {image_path}')
    
    print(f'Checked default events. Total events: {Event.objects.count()}')
except Exception as e:
    print(f'Error checking default events: {str(e)}')
"""

echo "Build completed successfully!"
