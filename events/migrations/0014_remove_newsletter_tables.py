from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration removes all newsletter-related tables.
    """

    dependencies = [
        ('events', '0013_remove_mailersend_field'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DROP TABLE IF EXISTS events_newslettercampaign;
            DROP TABLE IF EXISTS events_newslettertemplate;
            DROP TABLE IF EXISTS events_newsletter;
            """,
            reverse_sql="SELECT 1;",  # No-op for reverse
        ),
    ]
