from django.db import models
from django.utils.timezone import now
from django_fsm import FSMField, transition
from django_utils.choices import Choices, Choice

from apollo.users.models import User


class Election(models.Model):
    class State(Choices):
        CREATED = Choice("0", "CREATED")
        OPENED = Choice("1", "OPENED")
        FROZEN = Choice("2", "FROZEN")

    created_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(null=True)
    frozen_at = models.DateTimeField(null=True)
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
            * there is at least one question specified in the election
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
        self.opened_at = now()

    @transition(field=state, source=State.OPENED, target=State.FROZEN)
    def freeze(self) -> None:
        self.frozen_at = now()

    @property
    def state_string(self) -> str:
        return str(Election.State.choices[self.state])