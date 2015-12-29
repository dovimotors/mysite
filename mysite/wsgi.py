"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

base = os.path.dirname(os.path.dirname(__file__))
base_parent = os.path.dirname(base)
sys.path.append(base)
sys.path.append(base_parent)

sys.path.append('c:\apps\mysite')

os.environ.setdefault("PYTHON_EGG_CACHE", "c:\apps\mysite\Django-1.8.7-py2.7.egg")

os.environ["DJANGO_SETTINGS_MODULE"] = "mysite.settings"

application = get_wsgi_application()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
