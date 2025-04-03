"""
Script to ensure data persistence on Render.
This script performs checks and maintenance operations to ensure database connections
are properly established and maintained.
"""
import os
import sys
import django
import logging
import time
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('persistence_check')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myday.settings')

# Log environment variables (without sensitive data)
def log_env_vars():
    """Log relevant environment variables."""
    env_vars = {
        'DEBUG': os.environ.get('DEBUG', 'Not set'),
        'DJANGO_SETTINGS_MODULE': os.environ.get('DJANGO_SETTINGS_MODULE', 'Not set'),
        'ALLOWED_HOSTS': os.environ.get('ALLOWED_HOSTS', 'Not set'),
        'DATABASE_URL': 'Set (PostgreSQL)' if os.environ.get('DATABASE_URL') and 'postgres' in os.environ.get('DATABASE_URL', '') else 'NOT SET or INVALID',
        'PYTHON_VERSION': os.environ.get('PYTHON_VERSION', 'Not set'),
    }
    
    logger.info("Environment variables:")
    for key, value in env_vars.items():
        logger.info(f"  {key}: {value}")

# Log environment variables before Django setup
log_env_vars()

# Check if DATABASE_URL is set, if not, this is a critical error
if not os.environ.get('DATABASE_URL'):
    logger.critical("DATABASE_URL environment variable is not set!")
    logger.critical("This will cause data loss as the application will use SQLite.")
    logger.critical("Please configure the DATABASE_URL in your Render dashboard:")
    logger.critical("1. Go to: Dashboard > Your Web Service > Environment > Environment Variables")
    logger.critical("2. Add a new environment variable:")
    logger.critical("   Key: DATABASE_URL")
    logger.critical("   Value: postgresql://mydays_n59u_user:KX35eUaw9CqUeV03GQeyXa3nqS1qfbCh@dpg-cvlf2kd6ubrc73bin8i0-a.oregon-postgres.render.com/mydays_n59u")
    logger.critical("3. Save changes and redeploy your service")
    # Don't exit here, continue with checks to provide more diagnostic info
elif 'postgres' not in os.environ.get('DATABASE_URL', ''):
    logger.warning("DATABASE_URL does not appear to be a PostgreSQL connection string!")

# Now set up Django
try:
    django.setup()
    logger.info("Django setup successful")
except Exception as e:
    logger.error(f"Django setup failed: {e}")
    sys.exit(1)

from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import User
from django.conf import settings

def check_database_connection(max_retries=5, retry_delay=3):
    """Check if database connection is working properly with retries."""
    for attempt in range(max_retries):
        try:
            # Try to connect to the database
            connection = connections['default']
            connection.ensure_connection()
            
            # Check database engine
            db_engine = settings.DATABASES['default']['ENGINE']
            logger.info(f"Using database engine: {db_engine}")
            
            if 'sqlite' in db_engine and not settings.DEBUG:
                logger.warning("Using SQLite in production is not recommended!")
            elif 'postgresql' in db_engine or 'postgres' in db_engine:
                logger.info("Using PostgreSQL database - good for production")
            
            # Check if there are any users in the database
            user_count = User.objects.count()
            logger.info(f"Found {user_count} users in the database")
            
            return True
        except OperationalError as e:
            logger.warning(f"Database connection attempt {attempt+1}/{max_retries} failed: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error(f"All database connection attempts failed: {e}")
                return False
        except Exception as e:
            logger.error(f"Unexpected database error: {e}")
            return False

def check_media_files():
    """Check if media directories exist and are accessible."""
    media_root = settings.MEDIA_ROOT
    static_root = settings.STATIC_ROOT
    
    if os.path.exists(media_root):
        logger.info(f"Media directory exists at {media_root}")
        # Count files in media directory
        media_files = sum([len(files) for _, _, files in os.walk(media_root)])
        logger.info(f"Found {media_files} files in media directory")
    else:
        logger.warning(f"Media directory does not exist at {media_root}")
        try:
            os.makedirs(media_root, exist_ok=True)
            logger.info(f"Created media directory at {media_root}")
        except Exception as e:
            logger.error(f"Failed to create media directory: {e}")
    
    if os.path.exists(static_root):
        logger.info(f"Static directory exists at {static_root}")
        # Count files in static directory
        static_files = sum([len(files) for _, _, files in os.walk(static_root)])
        logger.info(f"Found {static_files} files in static directory")
    else:
        logger.warning(f"Static directory does not exist at {static_root}")

def log_database_info():
    """Log information about the database configuration."""
    try:
        db_config = settings.DATABASES['default']
        logger.info(f"Database engine: {db_config.get('ENGINE', 'Not set')}")
        
        # Don't log the full connection details for security reasons
        if 'NAME' in db_config:
            logger.info(f"Database name: {db_config.get('NAME', 'Not set')}")
        if 'HOST' in db_config:
            host = db_config.get('HOST', '')
            # Only show part of the host for security
            if host:
                masked_host = host.split('.')[0] + '.***.***' if '.' in host else host
                logger.info(f"Database host: {masked_host}")
        
        logger.info(f"CONN_MAX_AGE: {db_config.get('CONN_MAX_AGE', 'Not set')}")
        logger.info(f"CONN_HEALTH_CHECKS: {db_config.get('CONN_HEALTH_CHECKS', 'Not set')}")
    except Exception as e:
        logger.error(f"Failed to log database info: {e}")

def log_system_info():
    """Log information about the system."""
    logger.info(f"DEBUG mode is {'ON' if settings.DEBUG else 'OFF'}")
    logger.info(f"Current time: {datetime.now().isoformat()}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Django version: {django.get_version()}")
    logger.info(f"Working directory: {os.getcwd()}")

if __name__ == "__main__":
    logger.info("Starting persistence check...")
    log_system_info()
    log_database_info()
    
    db_ok = check_database_connection()
    check_media_files()
    
    if db_ok:
        logger.info("Persistence check completed successfully")
        sys.exit(0)
    else:
        logger.error("Persistence check failed")
        sys.exit(1)
