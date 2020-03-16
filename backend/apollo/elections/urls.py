from django.urls import path
from apollo.elections.views import QuestionDetail, ElectionDetail, ElectionList


urlpatterns = [
    path("questions/<int:pk>", QuestionDetail.as_view(), name="questions"),
    path("elections/<int:pk>", ElectionDetail.as_view(), name="election_detail"),
    path("elections", ElectionList.as_view(), name="elections"),
]
