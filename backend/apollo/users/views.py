from django.contrib.auth.models import User

from rest_framework import viewsets

from apollo.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    # for showcase purposes
    queryset = User.objects.all()
    serializer_class = UserSerializer
