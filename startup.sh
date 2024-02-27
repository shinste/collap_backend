#!/bin/bash
echo "1"
# Redirect stdout and stderr to a log file
exec > >(tee -i /var/log/myapp.log)
exec 2>&1
echo "2"
# Run collectstatic
python manage.py collectstatic --noinput

echo "3"
# Run Gunicorn with your Django application
gunicorn --workers 2 collap.wsgi