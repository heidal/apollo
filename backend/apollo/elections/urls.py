from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apollo.elections.views import ElectionDetail, ElectionViewSet, QuestionDetail


router = DefaultRouter()
router.register("elections", ElectionViewSet)

urlpatterns = [
    path("question/<int:pk>", QuestionDetail.as_view(), name="questions"),
    path("election/<int:pk>", ElectionDetail.as_view(), name="election_detail"),
    path("", include(router.urls)),
]
