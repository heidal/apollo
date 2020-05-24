from django.db import models


class Vote(models.Model):
    answer = models.ForeignKey(
        "Answer", on_delete=models.CASCADE, blank=True, null=True, related_name="votes"
    )
    answer_ciphertext = models.CharField(max_length=400)
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="votes"
    )
    author = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="votes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
