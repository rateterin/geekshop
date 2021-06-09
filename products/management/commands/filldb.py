from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.management import call_command
import os
import re


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')

        file_list = os.listdir('products/fixtures')
        if not file_list:
            return
        file_list.sort()
        file_list = list(filter(lambda x: re.match('\d{3}_.+\.json$', x), file_list))

        for file in file_list:
            call_command('loaddata', file[:-5])

        super_user = User.objects.create_superuser('django', 'django@geekshop.local', 'geekbrains')
