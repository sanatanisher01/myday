from django.db import migrations, connection


def get_sql_for_vendor():
    """Return SQL that's compatible with the current database vendor"""
    if connection.vendor == 'sqlite':
        # SQLite version
        return {
            'check_newsletter_table': """
                CREATE TABLE IF NOT EXISTS events_newsletter (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email VARCHAR(254) NOT NULL UNIQUE,
                    name VARCHAR(100) NULL,
                    is_active BOOLEAN NOT NULL DEFAULT 1,
                    subscribed_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_sent DATETIME NULL
                );
            """,
            'check_template_table': """
                CREATE TABLE IF NOT EXISTS events_newslettertemplate (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    subject VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    is_default BOOLEAN NOT NULL DEFAULT 0,
                    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """,
            'check_campaign_table': """
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
            """,
            'create_default_template': """
                INSERT INTO events_newslettertemplate (name, subject, content, is_default)
                SELECT 'Default Newsletter Template', 'Newsletter from MyDay Events',
                '<!DOCTYPE html>
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
</html>', 1
                WHERE NOT EXISTS (SELECT 1 FROM events_newslettertemplate);
            """,
            'fix_migration_state': """
                -- This is a simplified version for SQLite
                -- Insert migration records if they don't exist
                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0014_newsletter_templates_campaigns', CURRENT_TIMESTAMP);

                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0015_default_newsletter_template', CURRENT_TIMESTAMP);

                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0016_fix_missing_newsletter_tables', CURRENT_TIMESTAMP);

                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0017_create_newsletter_models', CURRENT_TIMESTAMP);

                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0018_fix_duplicate_tables', CURRENT_TIMESTAMP);

                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0019_create_newsletter_tables_properly', CURRENT_TIMESTAMP);

                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0020_create_default_newsletter_template', CURRENT_TIMESTAMP);

                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0021_fix_migration_sequence', CURRENT_TIMESTAMP);

                INSERT OR IGNORE INTO django_migrations (app, name, applied)
                VALUES ('events', '0022_ensure_default_template', CURRENT_TIMESTAMP);
            """
        }
    else:  # PostgreSQL
        return {
            'check_newsletter_table': """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'events_newsletter'
                    ) THEN
                        CREATE TABLE events_newsletter (
                            id bigserial PRIMARY KEY,
                            email varchar(254) NOT NULL UNIQUE,
                            name varchar(100) NULL,
                            is_active boolean NOT NULL DEFAULT true,
                            subscribed_at timestamp with time zone NOT NULL DEFAULT now(),
                            last_sent timestamp with time zone NULL
                        );
                    END IF;
                END
                $$;
            """,
            'check_template_table': """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'events_newslettertemplate'
                    ) THEN
                        CREATE TABLE events_newslettertemplate (
                            id bigserial PRIMARY KEY,
                            name varchar(100) NOT NULL,
                            subject varchar(200) NOT NULL,
                            content text NOT NULL,
                            is_default boolean NOT NULL DEFAULT false,
                            created_at timestamp with time zone NOT NULL DEFAULT now(),
                            updated_at timestamp with time zone NOT NULL DEFAULT now()
                        );
                    END IF;
                END
                $$;
            """,
            'check_campaign_table': """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_name = 'events_newslettercampaign'
                    ) THEN
                        CREATE TABLE events_newslettercampaign (
                            id bigserial PRIMARY KEY,
                            name varchar(100) NOT NULL,
                            subject varchar(200) NOT NULL,
                            content text NOT NULL,
                            status varchar(20) NOT NULL DEFAULT 'draft',
                            scheduled_at timestamp with time zone NULL,
                            sent_at timestamp with time zone NULL,
                            created_at timestamp with time zone NOT NULL DEFAULT now(),
                            updated_at timestamp with time zone NOT NULL DEFAULT now(),
                            sent_count integer NOT NULL DEFAULT 0,
                            error_message text NULL,
                            template_id bigint NULL REFERENCES events_newslettertemplate(id) ON DELETE SET NULL
                        );
                    END IF;
                END
                $$;
            """,
            'create_default_template': """
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT FROM events_newslettertemplate
                    ) THEN
                        INSERT INTO events_newslettertemplate (
                            name, subject, content, is_default, created_at, updated_at
                        ) VALUES (
                            'Default Newsletter Template',
                            'Newsletter from MyDay Events',
                            '<!DOCTYPE html>
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
</html>',
                            true,
                            now(),
                            now()
                        );
                    END IF;
                END
                $$;
            """,
            'fix_migration_state': """
                DO $$
                DECLARE
                    migration_exists boolean;
                BEGIN
                    -- Check and insert migration records for all previous newsletter migrations
                    FOR i IN 14..22 LOOP
                        EXECUTE format('
                            SELECT EXISTS (
                                SELECT 1 FROM django_migrations
                                WHERE app = ''events'' AND name = ''00%s_%%''
                            )', i) INTO migration_exists;

                        IF NOT migration_exists THEN
                            CASE i
                                WHEN 14 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0014_newsletter_templates_campaigns', now());
                                WHEN 15 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0015_default_newsletter_template', now());
                                WHEN 16 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0016_fix_missing_newsletter_tables', now());
                                WHEN 17 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0017_create_newsletter_models', now());
                                WHEN 18 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0018_fix_duplicate_tables', now());
                                WHEN 19 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0019_create_newsletter_tables_properly', now());
                                WHEN 20 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0020_create_default_newsletter_template', now());
                                WHEN 21 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0021_fix_migration_sequence', now());
                                WHEN 22 THEN
                                    INSERT INTO django_migrations (app, name, applied)
                                    VALUES ('events', '0022_ensure_default_template', now());
                                ELSE
                                    -- Do nothing for other cases
                            END CASE;
                        END IF;
                    END LOOP;
                END
                $$;
            """
        }


class Migration(migrations.Migration):
    """
    This migration uses raw SQL to fix the newsletter tables issue once and for all.
    It checks if tables exist before trying to create them and ensures the migration state is correct.
    """

    dependencies = [
        ('events', '0018_fix_duplicate_tables'),
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get SQL for the current database vendor
        self.sql_statements = get_sql_for_vendor()

    operations = [
        # Check if Newsletter table exists and create it if it doesn't
        migrations.RunSQL(
            sql=lambda: get_sql_for_vendor()['check_newsletter_table'],
            reverse_sql="SELECT 1;",  # No-op for reverse
        ),

        # Check if NewsletterTemplate table exists and create it if it doesn't
        migrations.RunSQL(
            sql=lambda: get_sql_for_vendor()['check_template_table'],
            reverse_sql="SELECT 1;",  # No-op for reverse
        ),

        # Check if NewsletterCampaign table exists and create it if it doesn't
        migrations.RunSQL(
            sql=lambda: get_sql_for_vendor()['check_campaign_table'],
            reverse_sql="SELECT 1;",  # No-op for reverse
        ),

        # Create a default template if none exists
        migrations.RunSQL(
            sql=lambda: get_sql_for_vendor()['create_default_template'],
            reverse_sql="SELECT 1;",  # No-op for reverse
        ),

        # Fix migration state by ensuring all previous migrations are marked as applied
        migrations.RunSQL(
            sql=lambda: get_sql_for_vendor()['fix_migration_state'],
            reverse_sql="SELECT 1;",  # No-op for reverse
        ),
    ]
