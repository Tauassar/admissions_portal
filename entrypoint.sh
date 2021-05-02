#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py shell -c "from auth_app.models import CustomUserModel; CustomUserModel.objects.create_superuser('admin@admin.com', '1223')"
gunicorn admissions_portal.wsgi:application --bind 0.0.0.0:8000
