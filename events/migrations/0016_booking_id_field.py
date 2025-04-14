from django.db import migrations, models
import uuid


def generate_booking_ids(apps, schema_editor):
    # Get the Booking model from the app registry
    Booking = apps.get_model('events', 'Booking')

    # Loop through all bookings without a booking_id and generate one
    for booking in Booking.objects.filter(booking_id__isnull=True):
        booking.booking_id = str(uuid.uuid4())[:8].upper()
        booking.save(update_fields=['booking_id'])


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
        migrations.RunPython(generate_booking_ids, reverse_code=migrations.RunPython.noop),
    ]
