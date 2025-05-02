from rest_framework import serializers
from .models import Category
from core.utils import generate_unique_slug

class CategoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'parent', 'description', 'is_active']                                                                                                                                                                                   
        

    def create(self, validated_data):
        category = Category(**validated_data)
        category.slug = generate_unique_slug(category, 'name')
        category.is_active = True
        category.save()
        return category