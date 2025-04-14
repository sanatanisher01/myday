from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_cloudinary_storage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsletter',
            name='mailersend_id',
        ),
    ]
