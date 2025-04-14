#!/usr/bin/env python
"""
This is a simplified script to fix migration issues by marking all newsletter migrations as applied.
"""
import os
import sys
import django
from django.db import connection

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myday.settings')
django.setup()


def fix_migrations():
    """Fix migration issues by marking all newsletter migrations as applied."""
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
        
        # Mark all newsletter migrations as applied
        newsletter_migrations = [
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
        
        for migration in newsletter_migrations:
            # Check if migration already exists
            cursor.execute("""
                SELECT COUNT(*) FROM django_migrations
                WHERE app = 'events' AND name = %s;
            """, [migration])
            exists = cursor.fetchone()[0] > 0
            
            if not exists:
                print(f"Adding migration: {migration}")
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
    
    print("Migration fixes completed.")


if __name__ == "__main__":
    fix_migrations()
