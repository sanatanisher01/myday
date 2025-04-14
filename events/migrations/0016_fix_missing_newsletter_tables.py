from django.db import migrations, models
import django.db.models.deletion
from django.db import connection


def create_newsletter_tables(apps, schema_editor):
    """Create newsletter tables if they don't exist"""
    # Get the database vendor
    vendor = connection.vendor
    cursor = connection.cursor()

    # Check if NewsletterTemplate table exists
    if vendor == 'postgresql':
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'events_newslettertemplate'
            );
        """)
        template_table_exists = cursor.fetchone()[0]
    else:  # SQLite
        cursor.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='events_newslettertemplate';
        """)
        template_table_exists = cursor.fetchone()[0] > 0

    # Create NewsletterTemplate table if it doesn't exist
    if not template_table_exists:
        if vendor == 'postgresql':
            cursor.execute("""
                CREATE TABLE events_newslettertemplate (
                    id bigserial PRIMARY KEY,
                    name varchar(100) NOT NULL,
                    subject varchar(200) NOT NULL,
                    content text NOT NULL,
                    is_default boolean NOT NULL,
                    created_at timestamp with time zone NOT NULL,
                    updated_at timestamp with time zone NOT NULL
                );
            """)
        else:  # SQLite
            cursor.execute("""
                CREATE TABLE events_newslettertemplate (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    name varchar(100) NOT NULL,
                    subject varchar(200) NOT NULL,
                    content text NOT NULL,
                    is_default boolean NOT NULL,
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL
                );
            """)

    # Check if NewsletterCampaign table exists
    if vendor == 'postgresql':
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'events_newslettercampaign'
            );
        """)
        campaign_table_exists = cursor.fetchone()[0]
    else:  # SQLite
        cursor.execute("""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='events_newslettercampaign';
        """)
        campaign_table_exists = cursor.fetchone()[0] > 0

    # Create NewsletterCampaign table if it doesn't exist
    if not campaign_table_exists:
        if vendor == 'postgresql':
            cursor.execute("""
                CREATE TABLE events_newslettercampaign (
                    id bigserial PRIMARY KEY,
                    name varchar(100) NOT NULL,
                    subject varchar(200) NOT NULL,
                    content text NOT NULL,
                    status varchar(20) NOT NULL,
                    scheduled_at timestamp with time zone NULL,
                    sent_at timestamp with time zone NULL,
                    created_at timestamp with time zone NOT NULL,
                    updated_at timestamp with time zone NOT NULL,
                    sent_count integer NOT NULL,
                    error_message text NULL,
                    template_id bigint NULL REFERENCES events_newslettertemplate(id) ON DELETE SET NULL
                );
            """)
        else:  # SQLite
            cursor.execute("""
                CREATE TABLE events_newslettercampaign (
                    id integer PRIMARY KEY AUTOINCREMENT,
                    name varchar(100) NOT NULL,
                    subject varchar(200) NOT NULL,
                    content text NOT NULL,
                    status varchar(20) NOT NULL,
                    scheduled_at datetime NULL,
                    sent_at datetime NULL,
                    created_at datetime NOT NULL,
                    updated_at datetime NOT NULL,
                    sent_count integer NOT NULL,
                    error_message text NULL,
                    template_id integer NULL REFERENCES events_newslettertemplate(id) ON DELETE SET NULL
                );
            """)


def reverse_migration(apps, schema_editor):
    """Dummy reverse function - we don't want to drop tables on reverse"""
    # This is a no-op function that allows the migration to be reversed without doing anything
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_default_newsletter_template'),
    ]

    operations = [
        # This migration is a safety check to ensure the newsletter tables exist
        # It recreates the tables if they don't exist using a Python function
        # that works with both PostgreSQL and SQLite
        migrations.RunPython(create_newsletter_tables, reverse_migration),
    ]
