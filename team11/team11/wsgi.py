"""
WSGI config for team11 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if "TEAM11_SERVER_ENV" in os.environ: 
    print("gunicorn : use setting_server")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team11.settings_server')
else: 
    print("gunicorn : use setting (default)")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team11.settings')

application = get_wsgi_application()
