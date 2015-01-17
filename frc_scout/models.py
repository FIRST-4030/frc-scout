from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# Team model, super simple, just gives an
# easy way to see if team already exists
from django.db.models.signals import post_save


class Team(models.Model):
    team_number = models.IntegerField(max_length=5)
    team_name = models.TextField(max_length=100)

    def __str__(self):
        return str(self.team_number) + ": " + self.team_name


# Additional user attributes
class UserProfile(models.Model):
    # Each attached to one user
    user = models.OneToOneField(User)

    team = models.ForeignKey(Team, null=True)

    team_manager = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username