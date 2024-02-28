"""
WSGI config for collap project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import sys
import os
from waitress import serve

from django.core.wsgi import get_wsgi_application

import sys
sys.path.append('/mnt/d/Work/Software_Projects/collap_backend')


settings_module = 'collap.settings' 
# if 'WEBSITE_HOSTNAME' in os.environ else 'collap.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
from whitenoise import WhiteNoise
application = WhiteNoise(get_wsgi_application())

serve(application, port=8000)


# settings_module = 'collap.production' if 'WEBSITE_HOSTNAME' in os.environ else 'collap.settings'
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'collap.production')

# application = get_wsgi_application()

