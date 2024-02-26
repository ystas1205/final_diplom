from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth.models import User

from backend.serializers import UserSerializer

from backend.models import Contact


# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class UserView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)


class ContactView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'message': 'Требуется войти'},
                            status=status.HTTP_403_FORBIDDEN)
        contact = Contact.objects.filter(user=request.user.id)
        serializer = UserSerializer(contact, many=True)
        return Response(serializer.data)
