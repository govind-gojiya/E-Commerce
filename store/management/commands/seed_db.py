# For Custom command make management > commands inside files name is use as commands
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import connection
from typing import Any
import os


class Command(BaseCommand):
    help = 'Popultes the database with collections and products'

    def handle(self, *args: Any, **options: Any) -> str | None:
        print("Populating seed data for database...")
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'seed.sql')
        sql = Path(file_path).read_text()

        with connection.cursor() as cursor:
            cursor.execute(sql)
