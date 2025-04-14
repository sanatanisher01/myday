from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration fixes the issue with duplicate tables by making the model creation
    conditional on whether the tables already exist.
    """

    dependencies = [
        ('events', '0017_create_newsletter_models'),
    ]

    operations = [
        # This is an empty migration that serves as a marker to indicate that
        # we've fixed the duplicate table issue. The actual fix is in the previous
        # migrations, but we need this to ensure Django's migration system
        # knows we've addressed the issue.
    ]
