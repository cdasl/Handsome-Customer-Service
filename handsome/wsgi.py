"""
WSGI config for handsome project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from socketio import Middleware
from backend.socket import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "handsome.settings")

backend = get_wsgi_application()
application = Middleware(sio,backend)
