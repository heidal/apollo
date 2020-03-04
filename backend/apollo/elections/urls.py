from django.urls import path, include

from . import views


urlpatterns = [
    path("elections", views.index, name="index")
]
