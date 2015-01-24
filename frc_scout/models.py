from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


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


def get_current_time():
    return timezone.now()


class Match(models.Model):
    # References
    team = models.ForeignKey(Team)
    scout = models.ForeignKey(User)
    match_number = models.IntegerField()
    timestamp = models.DateTimeField(default=get_current_time)
    # TODO add location

    # Autonomous
    auto_start_x = models.DecimalField(max_digits=8, decimal_places=8)
    auto_start_y = models.DecimalField(max_digits=8, decimal_places=8)

    auto_yellow_stacked_totes = models.IntegerField(default=0)
    auto_yellow_moved_totes = models.IntegerField(default=0)
    auto_grey_acquired_totes = models.IntegerField(default=0)

    auto_step_center_acquired_bins = models.IntegerField(default=0)
    auto_ground_acquired_bins = models.IntegerField(default=0)
    auto_moved_bins = models.IntegerField(default=0)

    auto_moved_to_auto_zone = models.BooleanField(default=False)
    auto_no_auto = models.BooleanField(default=False)

    auto_fouls = models.IntegerField(default=0)
    auto_interference = models.IntegerField(default=0)

    # Teleoperated
    tele_picked_up_ground_upright_totes = models.IntegerField(default=0)
    tele_picked_up_upside_down_totes = models.IntegerField(default=0)
    tele_picked_up_sideways_totes = models.IntegerField(default=0)
    tele_picked_up_human_station_totes = models.IntegerField(default=0)

    tele_picked_up_sideways_bins = models.IntegerField(default=0)
    tele_picked_up_upright_bins = models.IntegerField(default=0)
    tele_picked_up_center_step_bins = models.IntegerField(default=0)

    tele_pushed_litter = models.IntegerField(default=0)
    tele_placed_in_bin_litter = models.IntegerField(default=0)

    tele_fouls = models.IntegerField(default=0)
    tele_knocked_over_stacks = models.IntegerField(default=0)

    tele_dead_bot = models.BooleanField(default=False)
    tele_shooter_jam = models.BooleanField(default=False)

    tele_foul_context = models.TextField()
    tele_misc_comments = models.TextField()


class ToteStack(models.Model):
    match = models.ForeignKey(Match)
    start_height = models.IntegerField(default=0)
    end_height = models.IntegerField(default=1)
    x = models.DecimalField(max_digits=8, decimal_places=8)
    y = models.DecimalField(max_digits=8, decimal_places=8)
    coop_stack = models.BooleanField(default=False)


class BinStack(models.Model):
    match = models.ForeignKey(Match)
    height = models.IntegerField(default=1)


class Location(models.Model):
    name = models.TextField()
