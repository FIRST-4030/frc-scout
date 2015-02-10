from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone

User._meta.get_field('email')._unique = True


class Location(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name


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

    message = models.TextField(null=True)

    def __str__(self):
        return self.user.username + " - " + self.user.get_full_name() + " - " + str(self.team.team_number)


def get_current_time():
    return timezone.now()


class Match(models.Model):
    # References
    team_number = models.IntegerField(max_length=5)
    scout = models.ForeignKey(User)
    match_number = models.IntegerField()
    timestamp = models.DateTimeField(default=get_current_time)
    location = models.ForeignKey(Location)

    # Autonomous
    auto_start_x = models.DecimalField(max_digits=8, decimal_places=8)
    auto_start_y = models.DecimalField(max_digits=8, decimal_places=8)

    auto_yellow_stacked_totes = models.IntegerField(default=0)
    auto_yellow_moved_totes = models.IntegerField(default=0)
    auto_grey_acquired_totes = models.IntegerField(default=0)

    auto_step_center_acquired_containers = models.IntegerField(default=0)
    auto_ground_acquired_containers = models.IntegerField(default=0)
    auto_moved_containers = models.IntegerField(default=0)

    auto_moved_to_auto_zone = models.BooleanField(default=False)
    auto_no_auto = models.BooleanField(default=False)

    auto_fouls = models.IntegerField(default=0)
    auto_interference = models.IntegerField(default=0)

    # Teleoperated
    tele_picked_up_ground_upright_totes = models.IntegerField(default=0)
    tele_picked_up_upside_down_totes = models.IntegerField(default=0)
    tele_picked_up_sideways_totes = models.IntegerField(default=0)
    tele_picked_up_human_station_totes = models.IntegerField(default=0)

    tele_picked_up_sideways_containers = models.IntegerField(default=0)
    tele_picked_up_upright_containers = models.IntegerField(default=0)
    tele_picked_up_center_step_containers = models.IntegerField(default=0)

    tele_pushed_litter = models.IntegerField(default=0)
    tele_placed_in_container_litter = models.IntegerField(default=0)

    tele_fouls = models.IntegerField(default=0)
    tele_knocked_over_stacks = models.IntegerField(default=0)

    tele_dead_bot = models.BooleanField(default=False)
    tele_shooter_jam = models.BooleanField(default=False)

    tele_foul_context = models.TextField()
    tele_public_comments = models.TextField()

    def __str__(self):
        return str("Team: %i | Match: %i | Location: %s" % (self.team_number, self.match_number, self.location.name))


class ToteStack(models.Model):
    match = models.ForeignKey(Match)
    start_height = models.IntegerField(default=0)
    totes_added = models.IntegerField(default=0)
    x = models.DecimalField(max_digits=8, decimal_places=8)
    y = models.DecimalField(max_digits=8, decimal_places=8)
    coop_stack = models.BooleanField(default=False)

    def __str__(self):
        return str("Team: %i | Match: %i | Location: %s" % (self.match.team_number, self.match.match_number, self.match.location.name))


class ContainerStack(models.Model):
    match = models.ForeignKey(Match)
    height = models.IntegerField(default=1)

    def __str__(self):
        return str("Team: %i | Match: %i | Location: %s" % (self.match.team_number, self.match.match_number, self.match.location.name))


class PitScoutData(models.Model):
    scout = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    team_number = models.IntegerField(max_length=5)
    team_name = models.TextField(max_length=64, default=None, null=True)
    team_website = models.TextField(max_length=128, default=None, null=True)

    robot_height = models.FloatField(null=True)
    robot_weight = models.FloatField(null=True)
    robot_speed = models.FloatField(null=True)

    driver_1 = models.TextField(max_length=64, default=None, null=True)
    driver_2 = models.TextField(max_length=64, default=None, null=True)
    coach = models.TextField(max_length=64, default=None, null=True)

    # autonomous
    can_move_totes = models.NullBooleanField(null=True)
    can_move_containers = models.NullBooleanField(null=True)
    can_acquire_containers = models.NullBooleanField(null=True)
    auto_start_x = models.FloatField(null=True)
    auto_start_y = models.FloatField(null=True)

    # teleoperated
    tote_stack_capacity = models.IntegerField(max_length=3, default=None, null=True)

    # human interaction
    human_tote_loading = models.NullBooleanField(null=True)
    human_litter_loading = models.NullBooleanField(null=True)
    human_litter_throwing = models.NullBooleanField(null=True)

    # maneuvering
    has_turret = models.NullBooleanField(null=True)
    has_strafing = models.NullBooleanField(null=True)

    # other
    known_strengths = models.TextField(max_length=256, null=True)
    known_weaknesses = models.TextField(max_length=256, null=True)

    def __str__(self):
        rt = self.scout.get_short_name() + " | " + str(self.location.name) + " | " + str(self.team_number)

        if self.scout.userprofile.team.team_number == self.team_number:
            rt += " (SELF)"

        return rt
