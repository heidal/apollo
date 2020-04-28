from django.db import models
from django_fsm import FSMField, transition
from django_utils.choices import Choices, Choice

from apollo.users.models import User


class Election(models.Model):
    class State(Choices):
        CREATED = Choice("0", "CREATED")
        OPENED = Choice("1", "OPENED")
        FROZEN = Choice("2", "FROZEN")

    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="elections")
    state = FSMField(default=State.CREATED)

    class Meta:
        ordering = ["created_at"]

    def can_be_opened(self) -> bool:
        """
        Check if the election fulfills the requirements to be opened.

        The list of requirements:
            * there is at leas one question specified in the election
            * each question has at least one answer

        :return: True if the election can be opened, else False.
        """
        return (
            self.questions.all().exists()
            and not self.questions.filter(answers__isnull=True).exists()
        )

    @transition(
        field=state,
        source=State.CREATED,
        target=State.OPENED,
        conditions=[can_be_opened],
    )
    def open(self) -> None:
        # nothing to do for now
        pass

    @transition(field=state, source=State.OPENED, target=State.FROZEN)
    def freeze(self) -> None:
        # nothing to do for now
        pass
