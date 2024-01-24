"""
WSGI config for collap project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import sys
import os

from django.core.wsgi import get_wsgi_application

import sys
sys.path.append('/mnt/d/Work/Software_Projects/collap_backend')


print(f"DJANGO_SETTINGS_MODULE before: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collap.production')
os.environ['DJANGO_SETTINGS_MODULE'] = 'collap.production'

print(f"DJANGO_SETTINGS_MODULE after: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

# settings_module = 'collap.production' if 'WEBSITE_HOSTNAME' in os.environ else 'collap.settings'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collap.production')

application = get_wsgi_application()

