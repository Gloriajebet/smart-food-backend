from zipfile import ZipFile
import pandas as pd

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from foodsystem.models import Recipe


class Command(BaseCommand):
    help = "Import Kaggle recipes"

    def handle(self, *args, **kwargs):
        zip_file = ZipFile("food_recipes.csv.zip")
        csv_file = zip_file.namelist()[0]
        df = pd.read_csv(zip_file.open(csv_file))
        user = User.objects.get(username="Gloria Masit")
        imported = 0

        for _, row in df.iterrows():

            Recipe.objects.get_or_create(
                user=user,
                name=str(row["recipe_title"]),
                defaults={
                    "category": str(row["course"]),
                    "ingredients": str(row["ingredients"]),
                    "instructions": str(row["instructions"]),
                    "cooking_time": 30,
                    "servings": 4,
                }
            )
            imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{imported} recipes imported successfully."
            )
        )