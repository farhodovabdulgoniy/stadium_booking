from rest_framework import serializers
from . models import (
    Stadium,
    Book,
)


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
    
    



