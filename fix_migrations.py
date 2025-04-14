#!/usr/bin/env python
"""
This script fixes migration issues by directly manipulating the database.
It should be run before applying migrations.
"""
import os
import sys
import django
from django.db import connection

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myday.settings')
django.setup()


def fix_migrations():
    """Fix migration issues by directly manipulating the database."""
    print("Fixing migration issues...")
    
    # Check if we're using PostgreSQL
    is_postgres = connection.vendor == 'postgresql'
    
    with connection.cursor() as cursor:
        # Check if django_migrations table exists
        if is_postgres:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'django_migrations'
                );
            """)
            table_exists = cursor.fetchone()[0]
        else:  # SQLite
            cursor.execute("""
                SELECT COUNT(*) FROM sqlite_master 
                WHERE type='table' AND name='django_migrations';
            """)
            table_exists = cursor.fetchone()[0] > 0
        
        if not table_exists:
            print("django_migrations table doesn't exist yet. No fixes needed.")
            return
        
        # Get all events migrations
        cursor.execute("""
            SELECT id, app, name, applied FROM django_migrations
            WHERE app = 'events'
            ORDER BY name;
        """)
        migrations = cursor.fetchall()
        
        # Print current migrations
        print("Current migrations:")
        for migration in migrations:
            print(f"  {migration[1]}.{migration[2]} (applied: {migration[3]})")
        
        # Check for duplicate migrations
        migration_names = [m[2] for m in migrations]
        duplicates = set([x for x in migration_names if migration_names.count(x) > 1])
        
        if duplicates:
            print(f"Found duplicate migrations: {duplicates}")
            for dup in duplicates:
                # Get all instances of this migration
                cursor.execute("""
                    SELECT id FROM django_migrations
                    WHERE app = 'events' AND name = %s
                    ORDER BY id;
                """, [dup])
                dup_ids = [row[0] for row in cursor.fetchall()]
                
                # Keep the first one, delete the rest
                if len(dup_ids) > 1:
                    for dup_id in dup_ids[1:]:
                        print(f"Deleting duplicate migration with id {dup_id}")
                        cursor.execute("""
                            DELETE FROM django_migrations
                            WHERE id = %s;
                        """, [dup_id])
        
        # Check for missing migrations
        required_migrations = [
            '0001_initial',
            '0002_event_image',
            '0003_alter_event_image',
            '0004_subevent',
            '0005_alter_subevent_options_alter_subevent_event',
            '0006_review',
            '0007_booking',
            '0008_userprofile',
            '0009_contactmessage',
            '0010_galleryitem',
            '0011_increase_image_field_length',
            '0012_cloudinary_storage',
            '0013_remove_mailersend_field',
            '0014_newsletter_templates_campaigns',
            '0015_default_newsletter_template',
            '0016_fix_missing_newsletter_tables',
            '0017_create_newsletter_models',
            '0018_fix_duplicate_tables',
            '0019_create_newsletter_tables_properly',
            '0020_create_default_newsletter_template',
            '0021_fix_migration_sequence',
            '0022_ensure_default_template',
            '0023_fix_newsletter_tables_final',
            '0024_merge_20240601_0001',
            '0025_final_newsletter_fix',
        ]
        
        existing_migrations = set(migration_names)
        missing_migrations = [m for m in required_migrations if m not in existing_migrations]
        
        if missing_migrations:
            print(f"Found missing migrations: {missing_migrations}")
            for migration in missing_migrations:
                print(f"Adding missing migration: {migration}")
                if is_postgres:
                    cursor.execute("""
                        INSERT INTO django_migrations (app, name, applied)
                        VALUES ('events', %s, NOW());
                    """, [migration])
                else:  # SQLite
                    cursor.execute("""
                        INSERT INTO django_migrations (app, name, applied)
                        VALUES ('events', ?, CURRENT_TIMESTAMP);
                    """, [migration])
        
        # Check for newsletter tables
        tables_to_check = ['events_newsletter', 'events_newslettertemplate', 'events_newslettercampaign']
        for table in tables_to_check:
            if is_postgres:
                cursor.execute(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = '{table}'
                    );
                """)
                table_exists = cursor.fetchone()[0]
            else:  # SQLite
                cursor.execute(f"""
                    SELECT COUNT(*) FROM sqlite_master 
                    WHERE type='table' AND name='{table}';
                """)
                table_exists = cursor.fetchone()[0] > 0
            
            print(f"Table {table} exists: {table_exists}")
    
    print("Migration fixes completed.")


if __name__ == "__main__":
    fix_migrations()
