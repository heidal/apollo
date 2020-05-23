from rest_framework.routers import DefaultRouter

from apollo.elections import views


app_name = "elections"

router = DefaultRouter()
router.register("answers", views.AnswerViewSet)
router.register("elections", views.ElectionViewSet, basename="election")
router.register("questions", views.QuestionViewSet)
router.register("votes", views.VoteViewSet)

urlpatterns = router.urls
