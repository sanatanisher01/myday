"""
Script to ensure data persistence on Render.
This script performs checks and maintenance operations to ensure database connections
are properly established and maintained.
"""
import os
import sys
import django
import logging
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
django.setup()

from django.db import connections
from django.db.utils import OperationalError
from django.contrib.auth.models import User
from django.conf import settings

def check_database_connection():
    """Check if database connection is working properly."""
    try:
        # Try to connect to the database
        connection = connections['default']
        connection.ensure_connection()
        logger.info("✅ Database connection successful")
        
        # Check if there are any users in the database
        user_count = User.objects.count()
        logger.info(f"Found {user_count} users in the database")
        
        return True
    except OperationalError as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

def check_media_files():
    """Check if media directories exist and are accessible."""
    media_root = settings.MEDIA_ROOT
    static_root = settings.STATIC_ROOT
    
    if os.path.exists(media_root):
        logger.info(f"✅ Media directory exists at {media_root}")
        # Count files in media directory
        media_files = sum([len(files) for _, _, files in os.walk(media_root)])
        logger.info(f"Found {media_files} files in media directory")
    else:
        logger.warning(f"⚠️ Media directory does not exist at {media_root}")
        try:
            os.makedirs(media_root, exist_ok=True)
            logger.info(f"Created media directory at {media_root}")
        except Exception as e:
            logger.error(f"Failed to create media directory: {e}")
    
    if os.path.exists(static_root):
        logger.info(f"✅ Static directory exists at {static_root}")
    else:
        logger.warning(f"⚠️ Static directory does not exist at {static_root}")

def log_environment_info():
    """Log information about the environment."""
    logger.info(f"DATABASE_URL is {'set' if os.environ.get('DATABASE_URL') else 'NOT set'}")
    logger.info(f"DEBUG mode is {'ON' if settings.DEBUG else 'OFF'}")
    logger.info(f"Using database engine: {settings.DATABASES['default']['ENGINE']}")
    logger.info(f"CONN_MAX_AGE: {settings.DATABASES['default'].get('CONN_MAX_AGE', 'Not set')}")
    logger.info(f"Current time: {datetime.now().isoformat()}")

if __name__ == "__main__":
    logger.info("Starting persistence check...")
    log_environment_info()
    db_ok = check_database_connection()
    check_media_files()
    
    if db_ok:
        logger.info("✅ Persistence check completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ Persistence check failed")
        sys.exit(1)
