from django.contrib.auth.models import User
from rest_framework import serializers

# from backend.models import Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'email')



