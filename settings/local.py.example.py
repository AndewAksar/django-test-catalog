"""Template for local overrides.

Copy this file to ``settings/local.py`` and fill in environment variables or
hardcode values for local development. The ``.example`` suffix keeps secrets
out of version control while still providing a ready-to-use template.
"""

import os

from .cache import CACHES
from .core import DATABASES, TEMPLATES

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
TEMPLATES[0]['OPTIONS'].update({'debug': DEBUG})

ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', '*').split(',') if host.strip()]
INTERNAL_IPS = tuple(ip.strip() for ip in os.getenv('INTERNAL_IPS', '127.0.0.1,localhost').split(',') if ip.strip())

DATABASES['default']['HOST'] = os.getenv('POSTGRES_HOST', DATABASES['default']['HOST'])
DATABASES['default']['PORT'] = int(os.getenv('POSTGRES_PORT', DATABASES['default']['PORT']))
DATABASES['default']['USER'] = os.getenv('POSTGRES_USER', DATABASES['default']['USER'])
DATABASES['default']['PASSWORD'] = os.getenv('POSTGRES_PASSWORD', '')
DATABASES['default']['NAME'] = os.getenv('POSTGRES_DB', DATABASES['default']['NAME'])

redis_host = os.getenv('REDIS_HOST', '127.0.0.1')
redis_port = os.getenv('REDIS_PORT', '6379')
CACHES['default']['LOCATION'] = f'redis://{redis_host}:{redis_port}/0'
CACHES['session']['LOCATION'] = f'redis://{redis_host}:{redis_port}/1'
CACHES['queue']['LOCATION'] = f'redis://{redis_host}:{redis_port}/2'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
