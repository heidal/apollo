import abc

from rest_framework import serializers


class AuthorizedSerializer(serializers.Serializer):
    @abc.abstractmethod
    def authorize(self, attrs):
        pass

    def validate(self, attrs):
        attrs = super().validate(attrs)
        self.authorize(attrs)
        return attrs
