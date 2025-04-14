from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration merges the two leaf nodes in the migration graph:
    - 0022_ensure_default_template
    - 0023_fix_newsletter_tables_final
    """

    dependencies = [
        ('events', '0022_ensure_default_template'),
        ('events', '0023_fix_newsletter_tables_final'),
    ]

    operations = [
        # No operations needed, this is just a merge migration
    ]
