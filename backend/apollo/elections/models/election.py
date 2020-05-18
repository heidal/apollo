import regex

from django.db import models
from django.utils.timezone import now
from django_fsm import FSMField, transition
from django_utils.choices import Choices, Choice
from nacl.public import PrivateKey
from nacl.encoding import Base64Encoder

from apollo.users.models import User


class Election(models.Model):
    class State(Choices):
        CREATED = Choice("0", "CREATED")
        OPENED = Choice("1", "OPENED")
        CLOSED = Choice("2", "CLOSED")

    created_at = models.DateTimeField(auto_now_add=True)
    opened_at = models.DateTimeField(null=True)
    closed_at = models.DateTimeField(null=True)
    description = models.TextField()
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="elections")
    state = FSMField(default=State.CREATED)
    public_key = models.CharField(max_length=64, null=True, blank=False)
    secret_key = models.CharField(max_length=64, null=True, blank=False)

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
        sk = PrivateKey.generate()
        self.secret_key = sk.encode(Base64Encoder()).decode("ascii")
        self.public_key = sk.public_key.encode(Base64Encoder()).decode("ascii")
        self.opened_at = now()

    @transition(field=state, source=State.OPENED, target=State.CLOSED)
    def close(self) -> None:
        self.closed_at = now()

    @property
    def state_string(self) -> str:
        return str(Election.State.choices[self.state])


class VoterAuthorizationRule(models.Model):
    class Type(Choices):
        EXACT = Choice(0, "EXACT")
        REGEX = Choice(1, "REGEX")

    election = models.ForeignKey(
        Election, on_delete=models.CASCADE, related_name="authorization_rules"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.IntegerField(choices=Type)
    value = models.CharField(max_length=100)

    def is_authorized(self, name: str) -> bool:
        if self.type == self.Type.EXACT:
            return self.value == name
        elif self.type == self.Type.REGEX:
            return regex.fullmatch(self.value, name) is not None
