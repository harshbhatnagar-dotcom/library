"""
WSGI config for library project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import subprocess

from django.core.wsgi import get_wsgi_application
# Auto-run collectstatic only if staticfiles is empty (safe for Render free tier)
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'staticfiles')
if not os.path.exists(static_dir) or not os.listdir(static_dir):
    subprocess.call(['python', 'manage.py', 'collectstatic', '--noinput'])


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

application = get_wsgi_application()
