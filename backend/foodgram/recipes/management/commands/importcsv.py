import csv
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredients


class Command(BaseCommand):
    """Обработчик менеджмент-команды по импорту csv-данных в БД SQLite."""
    def handle(self, *args, **options):
        Ingredients.objects.all().delete()
        with open(os.path.join("data", "ingredients.csv"), 'r', encoding='utf-8') as fin:
            dr = csv.DictReader(fin)
            for i in dr:
                Ingredients.objects.get_or_create(
                    name=i['name'],
                    measurement_unit=i['measurement_unit']
                )
