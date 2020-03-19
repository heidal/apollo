from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apollo.users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    # for showcase purposes
    queryset = User.objects.all()
    serializer_class = UserSerializer
