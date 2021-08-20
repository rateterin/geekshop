#!/bin/sh

cd $(dirname $0)
python3 -m venv ../venv
. ./../venv/bin/activate
apt update && apt install graphviz -y
pip install --upgrade pip
pip install --no-cache-dir wheel
pip install --no-cache-dir -r ./requirements.txt
sleep 10

python manage.py makemigrations
python manage.py makemigrations adm
python manage.py makemigrations authapp
python manage.py makemigrations baskets
python manage.py makemigrations ordersapp
python manage.py makemigrations products
python manage.py makemigrations debug_toolbar
python manage.py makemigrations template_profiler_panel
python manage.py migrate
python manage.py collectstatic --noinput
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('django', 'geekshop@ter52.ru', 'geekbrains', age=42)" | python manage.py shell
python manage.py loaddata db.json
gunicorn --bind 0.0.0.0:8000 -w 3 geekshop.wsgi:application

exec "$@"
