#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infosis_site.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
#  python manage.py runserver
# python manage.py createsuperuser
# http://127.0.0.1:8000/admin/