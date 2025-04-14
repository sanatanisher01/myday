from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0010_newsletter_alter_activitylog_action_type_and_more'),  # Updated to match existing migration
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(max_length=500, upload_to='events/'),
        ),
        migrations.AlterField(
            model_name='subevent',
            name='image',
            field=models.ImageField(max_length=500, upload_to='subevents/'),
        ),
        migrations.AlterField(
            model_name='subeventcategory',
            name='image',
            field=models.ImageField(max_length=500, upload_to='categories/'),
        ),
        migrations.AlterField(
            model_name='galleryitem',
            name='image',
            field=models.ImageField(max_length=500, upload_to='gallery/'),
        ),
        migrations.AlterField(
            model_name='review',
            name='image',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='reviews/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, max_length=500, null=True, upload_to='avatars/'),
        ),
    ]
