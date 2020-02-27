from django.urls import path, include
from rest_framework import routers

from apollo.users.views import UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)

apipatterns = [
    path('', include(router.urls)),
]

urlpatterns = [
    path('api/', include(apipatterns))
]