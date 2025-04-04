# Generated by Django 4.2.10 on 2025-04-01 04:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_rename_avatar_userprofile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubEventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(upload_to='categories/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='events.subevent')),
            ],
            options={
                'verbose_name_plural': 'Sub-event categories',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='GalleryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery/')),
                ('caption', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_items', to='events.subevent')),
            ],
            options={
                'ordering': ['order', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('booking_date', models.DateField(blank=True, null=True)),
                ('booking_time', models.TimeField(blank=True, null=True)),
                ('guests', models.PositiveIntegerField(default=1)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.subeventcategory')),
                ('subevent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.subevent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
