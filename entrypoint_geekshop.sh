#!/bin/sh

cd ~/$(DOMAIN_NAME)/

pip install --no-cache-dir -r ./requirements.txt

sleep 10

python manage.py makemigrations
#python manage.py makemigrations adm
#python manage.py makemigrations authapp
#python manage.py makemigrations baskets
#python manage.py makemigrations ordersapp
#python manage.py makemigrations products
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 -w 3 testwebservice.wsgi:application

exec "$@"