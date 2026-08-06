from django.contrib.auth.models import User
from rest_framework import serializers 
from .models import FoodItem
from .models import Recipe

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'
        read_only_fields =["user"]

class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ["user"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        try:
            data["ingredients"] = instance.ingredient_list()
        except Exception as e:
            print("INGREDIENT ERROR:", e)
            data["ingredients"] = []

        return data