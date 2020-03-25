from django.urls import path, include
from rest_framework import routers

from apollo.users.views import UserViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = router.urls
