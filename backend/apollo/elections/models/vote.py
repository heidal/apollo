from django.db import models
from django.db.models import UniqueConstraint


class Vote(models.Model):
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE, related_name="votes")
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="votes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["answer", "author"], name="unique_answer_author")
        ]
