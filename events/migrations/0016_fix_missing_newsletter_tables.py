from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_default_newsletter_template'),
    ]

    operations = [
        # This migration is a safety check to ensure the newsletter tables exist
        # It recreates the tables if they don't exist
        
        # First, check if NewsletterTemplate exists, if not recreate it
        migrations.RunSQL(
            """
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
                        is_default boolean NOT NULL,
                        created_at timestamp with time zone NOT NULL,
                        updated_at timestamp with time zone NOT NULL
                    );
                END IF;
            END
            $$;
            """,
            reverse_sql=migrations.RunSQL.noop
        ),
        
        # Check if NewsletterCampaign exists, if not recreate it
        migrations.RunSQL(
            """
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
                        status varchar(20) NOT NULL,
                        scheduled_at timestamp with time zone NULL,
                        sent_at timestamp with time zone NULL,
                        created_at timestamp with time zone NOT NULL,
                        updated_at timestamp with time zone NOT NULL,
                        sent_count integer NOT NULL,
                        error_message text NULL,
                        template_id bigint NULL REFERENCES events_newslettertemplate(id) ON DELETE SET NULL
                    );
                END IF;
            END
            $$;
            """,
            reverse_sql=migrations.RunSQL.noop
        ),
    ]
