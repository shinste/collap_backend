#!/bin/bash

# Redirect stdout and stderr to a log file
exec > >(tee -i /var/log/myapp.log)
exec 2>&1

# Run collectstatic
python manage.py collectstatic --noinput

# Run Gunicorn with your Django application
gunicorn --workers 2 myproject.wsgi