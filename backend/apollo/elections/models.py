from django.contrib.auth.models import User
from django.db import models
from django.db.models import UniqueConstraint


class Election(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="elections")

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


class Vote(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="votes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["answer", "author"], name="unique_answer_author")
        ]
