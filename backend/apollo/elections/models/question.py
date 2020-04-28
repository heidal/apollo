from django.db import models


class Question(models.Model):
    election = models.ForeignKey(
        "Election", on_delete=models.CASCADE, related_name="questions"
    )
    question = models.CharField(max_length=200)
