from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import CategoryAddSerializer, CategoryListSerializer
from .models import Category
# Create your views here.

class CategoryAddView(APIView):
    """
    API view to add a new category.
    """
    def post(self, request):
        serializer = CategoryAddSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
