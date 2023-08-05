from rest_framework import serializers
from .models import Book, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'username', 'birth_year']

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'