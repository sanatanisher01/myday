#!/usr/bin/env python
"""
This script directly sets up the database tables needed for the newsletter functionality.
It bypasses Django's migration system to avoid errors with missing tables.
"""
import os
import sys
import django
from django.db import connection

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myday.settings')
django.setup()


def setup_database():
    """Set up the database tables directly."""
    print("Setting up database tables...")
    
    # Check if we're using PostgreSQL
    is_postgres = connection.vendor == 'postgresql'
    
    with connection.cursor() as cursor:
        # Create the newsletter tables if they don't exist
        if is_postgres:
            # Create Newsletter table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events_newsletter (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(254) NOT NULL UNIQUE,
                    name VARCHAR(100) NULL,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    subscribed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    last_sent TIMESTAMP WITH TIME ZONE NULL
                );
            """)
            
            # Create NewsletterTemplate table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events_newslettertemplate (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    subject VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    is_default BOOLEAN NOT NULL DEFAULT FALSE,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
                );
            """)
            
            # Create NewsletterCampaign table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events_newslettercampaign (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    subject VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'draft',
                    scheduled_at TIMESTAMP WITH TIME ZONE NULL,
                    sent_at TIMESTAMP WITH TIME ZONE NULL,
                    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
                    sent_count INTEGER NOT NULL DEFAULT 0,
                    error_message TEXT NULL,
                    template_id INTEGER NULL REFERENCES events_newslettertemplate(id) ON DELETE SET NULL
                );
            """)
        else:  # SQLite
            # Create Newsletter table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events_newsletter (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(254) NOT NULL UNIQUE,
                    name VARCHAR(100) NULL,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    subscribed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_sent DATETIME NULL
                );
            """)
            
            # Create NewsletterTemplate table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events_newslettertemplate (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    subject VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    is_default BOOLEAN NOT NULL DEFAULT 0,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create NewsletterCampaign table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events_newslettercampaign (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    subject VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    status VARCHAR(20) NOT NULL DEFAULT 'draft',
                    scheduled_at DATETIME NULL,
                    sent_at DATETIME NULL,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    sent_count INTEGER NOT NULL DEFAULT 0,
                    error_message TEXT NULL,
                    template_id INTEGER NULL REFERENCES events_newslettertemplate(id) ON DELETE SET NULL
                );
            """)
        
        # Check if default template exists
        cursor.execute("SELECT COUNT(*) FROM events_newslettertemplate;")
        template_count = cursor.fetchone()[0]
        
        if template_count == 0:
            # Create default template
            default_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyDay Events Newsletter</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f9f9f9;
        }
        
        .container {
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        .header {
            background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        
        .content {
            padding: 20px;
        }
        
        .footer {
            background-color: #f5f5f5;
            padding: 20px;
            text-align: center;
            font-size: 14px;
            color: #666;
        }
        
        .button {
            display: inline-block;
            background-color: #4e73df;
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 4px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{{ subject }}</h1>
        </div>
        
        <div class="content">
            <p>Hello {{ name|default:"there" }},</p>
            
            <div>{{ custom_message }}</div>
            
            <p>Thank you for subscribing to our newsletter!</p>
            
            <div style="text-align: center;">
                <a href="https://myday-kokr.onrender.com/events/" class="button">Visit Our Website</a>
            </div>
        </div>
        
        <div class="footer">
            <p>Best regards,<br>MyDay Events Team</p>
            <p>&copy; 2024 MyDay Events. All rights reserved.</p>
            <p>
                <a href="{{ unsubscribe_url }}">Unsubscribe</a> from this newsletter
            </p>
        </div>
    </div>
</body>
</html>"""
            
            if is_postgres:
                cursor.execute("""
                    INSERT INTO events_newslettertemplate (name, subject, content, is_default, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, NOW(), NOW());
                """, ["Default Newsletter Template", "Newsletter from MyDay Events", default_template, True])
            else:  # SQLite
                cursor.execute("""
                    INSERT INTO events_newslettertemplate (name, subject, content, is_default)
                    VALUES (?, ?, ?, ?);
                """, ["Default Newsletter Template", "Newsletter from MyDay Events", default_template, 1])
            
            print("Created default newsletter template.")
        
        # Mark all migrations as applied
        migrations_to_mark = [
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
        
        # Check if django_migrations table exists
        if is_postgres:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'django_migrations'
                );
            """)
            migrations_table_exists = cursor.fetchone()[0]
        else:  # SQLite
            cursor.execute("""
                SELECT COUNT(*) FROM sqlite_master 
                WHERE type='table' AND name='django_migrations';
            """)
            migrations_table_exists = cursor.fetchone()[0] > 0
        
        if migrations_table_exists:
            for migration in migrations_to_mark:
                # Check if migration already exists
                cursor.execute("""
                    SELECT COUNT(*) FROM django_migrations
                    WHERE app = 'events' AND name = %s;
                """, [migration])
                exists = cursor.fetchone()[0] > 0
                
                if not exists:
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
                    print(f"Marked migration {migration} as applied.")
    
    print("Database setup completed successfully.")


if __name__ == "__main__":
    setup_database()
