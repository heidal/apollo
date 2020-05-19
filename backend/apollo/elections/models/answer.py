from django.db import models
from django.utils.timezone import now


class Answer(models.Model):
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=now)
