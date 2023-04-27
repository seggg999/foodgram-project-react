import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Добавляет данные из файлa ingredients.csv в таблицу Ingredient'

    def handle(self, *args, **options):
        print('\nCreating Ingredient list')
        with open(
            f'{settings.BASE_DIR}/static/data/ingredients.csv',
                'r',
                encoding='utf-8'
        ) as csv_file:
            r = csv.DictReader(csv_file,
                               fieldnames=['name', 'measurement_unit'])

            for row in r:
                print(row['name'], ',', row['measurement_unit'])
                Ingredient.objects.get_or_create(
                    name=row['name'],
                    measurement_unit=row['measurement_unit'])
            print(' -List created\nDone')
