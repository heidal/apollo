from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # mostly for showcase purposes and to check that everything works
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]
