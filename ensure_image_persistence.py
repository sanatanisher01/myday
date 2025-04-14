#!/usr/bin/env python
"""
Script to ensure image persistence on Render.
This script checks for image references in the database and ensures they exist on the persistent disk.
"""

import os
import sys
import django
import shutil
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myday.settings')
django.setup()

from django.conf import settings
from django.core.files.storage import default_storage
from events.models import Event, SubEvent, Review, GalleryItem, SubEventCategory, UserProfile

def ensure_directory_exists(path):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(path, exist_ok=True)
    print(f"Ensured directory exists: {path}")

def copy_file_if_exists(src, dest):
    """Copy a file if it exists, creating the destination directory if necessary."""
    if not os.path.exists(src):
        print(f"Source file does not exist: {src}")
        return False

    dest_dir = os.path.dirname(dest)
    ensure_directory_exists(dest_dir)

    try:
        shutil.copy2(src, dest)
        print(f"Copied file: {src} -> {dest}")
        return True
    except Exception as e:
        print(f"Error copying file {src} to {dest}: {str(e)}")
        return False

def ensure_model_images(model_class, field_name='image'):
    """Ensure all images for a model exist on the persistent disk."""
    print(f"\nChecking {model_class.__name__} images...")
    count = 0
    for obj in model_class.objects.all():
        field = getattr(obj, field_name)
        if field:
            # Check if we're dealing with a CloudinaryResource
            if hasattr(field, 'public_id') and field.public_id:
                print(f"Cloudinary image found: {field.public_id}")
                count += 1
                continue

            # Handle regular ImageField
            if hasattr(field, 'name') and field.name:
                # Get the path to the image file
                try:
                    if hasattr(field, 'path'):
                        source_path = field.path
                    else:
                        # Skip if we can't get the path
                        print(f"Skipping image without path attribute")
                        continue

                    # If we're on Render, ensure the file exists in the persistent storage
                    if settings.ON_RENDER:
                        # Construct the destination path on the persistent disk
                        rel_path = field.name
                        dest_path = os.path.join(settings.MEDIA_ROOT, rel_path)

                        # If the file doesn't exist in persistent storage but exists elsewhere, copy it
                        if not os.path.exists(dest_path) and os.path.exists(source_path):
                            if copy_file_if_exists(source_path, dest_path):
                                count += 1
                        elif os.path.exists(dest_path):
                            print(f"File already exists in persistent storage: {dest_path}")
                        else:
                            print(f"File not found in any location: {field.name}")

                            # Try to find a default image
                            if 'events/' in field.name:
                                event_slug = os.path.basename(field.name).split('.')[0]
                                default_path = os.path.join(settings.MEDIA_ROOT, 'events', f'default-{event_slug}.jpg')
                                if os.path.exists(default_path):
                                    print(f"Using default image: {default_path}")
                                    # Update the model to use the default image
                                    field.name = f'events/default-{event_slug}.jpg'
                                    obj.save()
                                    count += 1
                except Exception as e:
                    print(f"Error processing image: {str(e)}")

    print(f"Processed {count} images for {model_class.__name__}")

def main():
    """Main function to ensure image persistence."""
    print("Starting image persistence check...")

    # Ensure media directories exist
    for subdir in ['events', 'subevents', 'reviews', 'avatars', 'gallery', 'categories']:
        ensure_directory_exists(os.path.join(settings.MEDIA_ROOT, subdir))

    # Ensure images for each model
    ensure_model_images(Event)
    ensure_model_images(SubEvent)
    ensure_model_images(Review)
    ensure_model_images(GalleryItem)
    ensure_model_images(SubEventCategory)
    ensure_model_images(UserProfile, 'profile_picture')

    print("\nImage persistence check completed.")

if __name__ == "__main__":
    main()
