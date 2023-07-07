from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']

    def validate_password(self, value):
        return make_password(value)