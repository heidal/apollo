from django.db import models
from django.utils.timezone import now


class Question(models.Model):
    election = models.ForeignKey(
        "Election", on_delete=models.CASCADE, related_name="questions"
    )
    question = models.CharField(max_length=200)
    created_at = models.DateTimeField(default=now)
