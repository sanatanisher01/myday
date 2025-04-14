from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fixes the migration state for newsletter tables'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Checking migration state...'))
        
        # Check if the tables exist
        tables_exist = self._check_tables_exist()
        
        if tables_exist:
            self.stdout.write(self.style.SUCCESS('Newsletter tables already exist. Fixing migration state...'))
            self._fix_migration_state()
        else:
            self.stdout.write(self.style.WARNING('Newsletter tables do not exist. No action needed.'))
    
    def _check_tables_exist(self):
        """Check if the newsletter tables exist"""
        with connection.cursor() as cursor:
            if connection.vendor == 'postgresql':
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'events_newsletter'
                    );
                """)
                newsletter_exists = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'events_newslettertemplate'
                    );
                """)
                template_exists = cursor.fetchone()[0]
            else:  # SQLite
                cursor.execute("""
                    SELECT COUNT(*) FROM sqlite_master 
                    WHERE type='table' AND name='events_newsletter';
                """)
                newsletter_exists = cursor.fetchone()[0] > 0
                
                cursor.execute("""
                    SELECT COUNT(*) FROM sqlite_master 
                    WHERE type='table' AND name='events_newslettertemplate';
                """)
                template_exists = cursor.fetchone()[0] > 0
        
        return newsletter_exists and template_exists
    
    def _fix_migration_state(self):
        """Fix the migration state in django_migrations table"""
        migrations_to_check = [
            '0014_newsletter_templates_campaigns',
            '0015_default_newsletter_template',
            '0016_fix_missing_newsletter_tables',
            '0017_create_newsletter_models',
            '0018_fix_duplicate_tables',
            '0019_create_newsletter_tables_properly',
            '0020_create_default_newsletter_template',
            '0021_fix_migration_sequence'
        ]
        
        with connection.cursor() as cursor:
            for migration in migrations_to_check:
                # Check if migration exists
                cursor.execute("""
                    SELECT COUNT(*) FROM django_migrations
                    WHERE app = 'events' AND name = %s;
                """, [migration])
                exists = cursor.fetchone()[0] > 0
                
                if not exists:
                    # Insert the migration record
                    self.stdout.write(f"Adding migration record for events.{migration}")
                    cursor.execute("""
                        INSERT INTO django_migrations (app, name, applied)
                        VALUES ('events', %s, NOW());
                    """, [migration])
                else:
                    self.stdout.write(f"Migration record for events.{migration} already exists")
        
        self.stdout.write(self.style.SUCCESS('Migration state fixed successfully!'))
