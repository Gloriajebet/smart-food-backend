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
    ingredients = serializers.SerializerMethodField()
    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ["user"]     

    def get_ingredients(self, obj):
        return obj.ingredient_list()   