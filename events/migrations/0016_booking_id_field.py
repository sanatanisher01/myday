from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_default_newsletter_template'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='booking_id',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
