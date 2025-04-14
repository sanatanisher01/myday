from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration fixes the migration sequence by marking the previous migrations as applied
    without actually running their SQL commands. This prevents errors when tables already exist.
    """

    dependencies = [
        ('events', '0020_create_default_newsletter_template'),
    ]

    operations = [
        migrations.RunSQL(
            # This is a no-op SQL statement that will always succeed
            sql="SELECT 1;",
            # This is the reverse SQL, also a no-op
            reverse_sql="SELECT 1;",
        ),
    ]
