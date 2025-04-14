from django.db import migrations


def remove_field_if_exists(apps, schema_editor):
    try:
        Newsletter = apps.get_model('events', 'Newsletter')
        # Check if the field exists before trying to remove it
        if hasattr(Newsletter, 'mailersend_id'):
            schema_editor.remove_field(Newsletter, Newsletter._meta.get_field('mailersend_id'))
    except Exception as e:
        print(f"Skipping mailersend_id removal: {str(e)}")


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_cloudinary_storage'),
    ]

    operations = [
        migrations.RunPython(remove_field_if_exists, migrations.RunPython.noop),
    ]
