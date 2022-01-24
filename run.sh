#!/bin/bash
#------------------------------------------
# run.sh
#------------------------------------------
# Apply Collect static
##echo "Collect static files"
##python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting api server"
#gunicorn med5_backend.wsgi:application --reload --workers 4 --bind 0.0.0.0:8000 --access-logfile /var/log/access.log --error-logfile /var/log/error.log
python manage.py runserver 0.0.0.0:8000