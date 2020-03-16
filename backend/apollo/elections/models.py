from django.db import models


class Answer(models.Model):
    text = models.CharField(max_length=200)
    votes = models.IntegerField()


class Question(models.Model):
    answers = models.ForeignKey(Answer, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)


class Election(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    class Meta:
        ordering = ["created"]
