from django.db import models
from django.contrib.auth.models import User

class FoodItem(models.Model):
    user = models.ForeignKey(
          User,
         on_delete=models.CASCADE,
         related_name="food_items"
         )
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    category = models.CharField(max_length=100)
    purchase_date = models.DateField()
    expiry_date = models.DateField()
    unit = models.CharField(max_length=50, blank=True, default='')  
    storage_location = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_used = models.BooleanField(default=False)
    used_date = models.DateField(blank=True, null=True)

class Recipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes"
    )

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=100)

    cooking_time = models.PositiveIntegerField(
        help_text="Cooking time in minutes"
    )

    servings = models.PositiveIntegerField()

    ingredients = models.TextField(
        help_text="One ingredient per line"
    )

    instructions = models.TextField()

    image = models.ImageField(
        upload_to="recipes/",
        blank=True,
        null=True
    )

    def ingredient_list(self):
        return [
            ingredient.strip()
            for ingredient in self.ingredients.split("\n")
            if ingredient.strip()
        ]

    def __str__(self):
        return self.name
