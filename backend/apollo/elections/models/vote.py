import base64
import hashlib
import secrets

from django.db import models
from django.db.models import UniqueConstraint

from apollo.elections.crypto import SEED_BIT_SIZE, SEED_BYTE_SIZE
from apollo.users.models import User


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

    def save(self, **kwargs):
        # TODO(adambudziak) this is not the best place for this
        super().save(**kwargs)
        Voter.objects.get_or_create(
            user=self.author,
            election=self.question.election
        )


class Voter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    election = models.ForeignKey('elections.Election', on_delete=models.CASCADE, null=False, related_name="voters")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    seed = models.BinaryField(max_length=SEED_BYTE_SIZE, null=False, editable=False)

    class Meta:
        constraints = [UniqueConstraint(fields=["user", "election"], name="Unique voter constraint")]

    def save(self, **kwargs):
        if self.seed is None:
            self.seed = secrets.randbits(SEED_BIT_SIZE).to_bytes(SEED_BYTE_SIZE, byteorder='big')
        super().save(**kwargs)

    @property
    def seed_hash(self) -> bytes:
        hasher = hashlib.sha3_256()
        election_seed_hash = self.election.seed_hash
        hasher.update(election_seed_hash)
        hasher.update(bytes(self.seed))
        return hasher.digest()

    @property
    def pseudonym(self) -> str:
        hasher = hashlib.sha3_256()
        hasher.update(self.seed_hash)
        hasher.update(self.user.email.encode('utf-8'))
        return base64.b64encode(hasher.digest())  # TODO(adambudziak) temporary, possibly we want a different encoding

    @property
    def vote_ciphertext_hash(self) -> str:
        hasher = hashlib.sha3_256()
        votes = self.user.votes.filter(question__election=self.election)
        for vote in votes:
            hasher.update(vote.answer_ciphertext.encode('utf-8'))
        return base64.b64encode(hasher.digest())
