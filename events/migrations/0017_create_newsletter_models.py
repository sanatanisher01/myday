from django.db import migrations, models, connection
import django.db.models.deletion
import django.utils.timezone


def table_exists(table_name):
    """Check if a table exists in the database"""
    with connection.cursor() as cursor:
        if connection.vendor == 'postgresql':
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = %s
                );
            """, [table_name])
            return cursor.fetchone()[0]
        else:  # SQLite
            cursor.execute("""
                SELECT COUNT(*) FROM sqlite_master
                WHERE type='table' AND name=%s;
            """, [table_name])
            return cursor.fetchone()[0] > 0


def skip_if_table_exists(apps, schema_editor, **kwargs):
    """Skip the migration operation if the table already exists"""
    model_name = kwargs.get('model_name')
    if model_name and table_exists(f'events_{model_name.lower()}'):
        return False  # Skip the operation
    return True  # Proceed with the operation


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_fix_missing_newsletter_tables'),
    ]

    operations = [
        # Create the Newsletter model if it doesn't exist
        migrations.RunSQL(
            sql="SELECT 1;",  # No-op SQL
            reverse_sql="SELECT 1;",  # No-op SQL
            state_operations=[
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
                ),
            ]
        ),

        # Create the NewsletterTemplate model if it doesn't exist
        migrations.RunSQL(
            sql="SELECT 1;",  # No-op SQL
            reverse_sql="SELECT 1;",  # No-op SQL
            state_operations=[
                migrations.CreateModel(
                    name='NewsletterTemplate',
                    fields=[
                        ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                        ('name', models.CharField(max_length=100)),
                        ('subject', models.CharField(max_length=200)),
                        ('content', models.TextField()),
                        ('is_default', models.BooleanField(default=False)),
                        ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                        ('updated_at', models.DateTimeField(auto_now=True)),
                    ],
                ),
            ]
        ),

        # Create the NewsletterCampaign model if it doesn't exist
        migrations.RunSQL(
            sql="SELECT 1;",  # No-op SQL
            reverse_sql="SELECT 1;",  # No-op SQL
            state_operations=[
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
                ),
            ]
        ),
    ]
