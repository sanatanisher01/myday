from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    """
    This migration creates the newsletter tables properly using Django's ORM.
    Previous migrations used RunSQL which can cause issues in some environments.
    """

    dependencies = [
        ('events', '0018_fix_duplicate_tables'),
    ]

    operations = [
        # Create the Newsletter model
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('subscribed_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_sent', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Newsletter Subscriber',
                'verbose_name_plural': 'Newsletter Subscribers',
                'ordering': ['-subscribed_at'],
            },
        ),
        
        # Create the NewsletterTemplate model
        migrations.CreateModel(
            name='NewsletterTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField(help_text="You can use HTML and template variables like {{ name }}, {{ custom_message }}, etc.")),
                ('is_default', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Newsletter Template',
                'verbose_name_plural': 'Newsletter Templates',
                'ordering': ['-updated_at'],
            },
        ),
        
        # Create the NewsletterCampaign model
        migrations.CreateModel(
            name='NewsletterCampaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('sending', 'Sending'), ('sent', 'Sent'), ('failed', 'Failed')], default='draft', max_length=20)),
                ('scheduled_at', models.DateTimeField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('sent_count', models.IntegerField(default=0)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('template', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.newslettertemplate')),
            ],
            options={
                'verbose_name': 'Newsletter Campaign',
                'verbose_name_plural': 'Newsletter Campaigns',
                'ordering': ['-created_at'],
            },
        ),
    ]
