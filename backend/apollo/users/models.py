from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    def __str__(self):
        return self.email

    @property
    def available_elections(self):
        from apollo.elections import models

        authorized_elections = models.VoterAuthorizationRule.objects.authorized(
            self
        ).values_list("election_id", flat=True)
        return models.Election.objects.filter(id__in=authorized_elections)
