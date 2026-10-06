from rest_framework import serializers
from .models import Book

# a ModelSerializer will automatically generate fields based on the model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields=['id', 'title', 'author', 'publish_date']



