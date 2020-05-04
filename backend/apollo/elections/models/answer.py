from django.db import models


class Answer(models.Model):
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=200)
