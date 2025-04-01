"""
WSGI config for myday project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

# Load environment variables from .env file if it exists
env_path = Path(__file__).resolve().parent.parent / '.env'
if env_path.exists():
    from dotenv import load_dotenv
    load_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myday.settings')

application = get_wsgi_application()
