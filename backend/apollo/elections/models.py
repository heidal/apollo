from django.db import models


class Election(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ["created_at"]


class Question(models.Model):
    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="questions"
    )
    question = models.CharField(max_length=200)


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
