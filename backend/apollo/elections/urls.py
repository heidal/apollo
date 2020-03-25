from rest_framework.routers import DefaultRouter

from apollo.elections.views import AnswerViewSet, ElectionViewSet, QuestionViewSet


app_name = "elections"

router = DefaultRouter()
router.register("answers", AnswerViewSet)
router.register("elections", ElectionViewSet)
router.register("questions", QuestionViewSet)

urlpatterns = router.urls
