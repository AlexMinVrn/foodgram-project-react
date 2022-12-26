import csv
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Обработчик менеджмент-команды по импорту csv-данных в БД SQLite."""
    def handle(self, *args, **options):
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()

        with open('data/ingredients.csv', 'r', encoding='utf8') as fin:
            dr = csv.DictReader(fin)
            to_db = [(i['name'], i['measurement_unit']) for i in dr]

        cursor.executemany(
            'INSERT INTO recipes_ingredients (name, measurement_unit) VALUES (?, ?);', to_db)
        connection.commit()
        connection.close()
