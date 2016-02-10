from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Create your models here.

User._meta.get_field('email')._unique = True


class Location(models.Model):
    name = models.TextField()
    tba_event_code = models.TextField(blank=True, null=True)
    venue_address = models.TextField(null=True)
    location = models.TextField(null=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    team_number = models.IntegerField(max_length=5)
    team_name = models.TextField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.team_number) + ": " + str(self.team_name)


# Additional user attributes
class UserProfile(models.Model):
    # Each attached to one user
    user = models.OneToOneField(User)

    team = models.ForeignKey(Team, null=True)
    team_manager = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    message = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username + " - " + self.user.get_full_name() + " - " + str(self.team.team_number)


def get_current_time():
    return timezone.now()


class Match(models.Model):
    class Meta:
        verbose_name_plural = "Matches"

    # provide everything after this
    """Sample here
    {
        "scout_team_number" : 1899,
        "scout_name" : "Twilight Sparkle",
        "no_show" : false,
        "team_number" : 1988
        "auto_start_x" : 100,
        "auto_start_y" : 100,
        "high_goals" : 9001,
        "low_goals" : 9001,
        "blocks_goals" : 9001,
        "crosses_goals" : 9001,
        "events" : [
            {...},
            {...},
        ]
    }
    """
    
    scout_team_number = models.IntegerField(max_length=5, null=True)
    scout_name = models.TextField(null=True)
    
    no_show = models.BooleanField(default=False)

    team_number = models.IntegerField(max_length=5)
    #you don't need to provide this
    scout = models.ForeignKey(User)
    #Get from either TBA or user input
    match_number = models.IntegerField()
    #Don't need this unless you wait to upload
    timestamp = models.DateTimeField(default=get_current_time)
    #don't provide this
    location = models.ForeignKey(Location)

    # Autonomous
    auto_start_x = models.DecimalField(default=0, max_digits=20, decimal_places=16)
    auto_start_y = models.DecimalField(default=0, max_digits=20, decimal_places=16)
    
    #averageable stats
    high_goals = models.IntegerField(max_length=3, default=0)
    low_goals = models.IntegerField(max_length=3, default=0)
    blocks = models.IntegerField(max_length=3, default=0)
    crosses = models.IntegerField(max_length=3, default=0)

    def __str__(self):
        return str("Team: %i | Match: %i | Location: %s" % (self.team_number, self.match_number, self.location.name))


class Event(models.Model):
    team_number = models.IntegerField(max_length=5)
    match = models.ForeignKey(Match)
    ev_num = models.IntegerField(max_length=2, default=0)
    #provide all of these, as approprite
    eventTypes = (
        (0,"LowGoal"),
        (1,"HighGoal"),
        (2,"Crossing"),
        (3,"PickupBall"),
        (4,"BlockedShot"),
        (5,"BlockedCrossing"),
        (6,"GameEnd")
        )
    #milliseconds since match start as time
    time = models.IntegerField(max_length=8)
    endTime = models.FloatField(null=True)
    evType = models.IntegerField(max_length=1,
                                choices=eventTypes,
                                default=0)
    nextEvType = models.IntegerField(max_length=1,
                                choices=eventTypes,
                                default=6)
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    isAuton = models.BooleanField(default=False)
class MatchPrivateComments(models.Model):
    class Meta:
        verbose_name_plural = "Match private comments"

    match = models.OneToOneField(Match)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return str("Team: %i | Match: %i | Location: %s" %
                   (self.match.team_number, self.match.match_number, self.match.location.name))

class PitScoutData(models.Model):
    class Meta:
        verbose_name_plural = "Pit scout data"

    scout = models.ForeignKey(User)
    location = models.ForeignKey(Location)
    #You need to provide everything after this
    pitscout_name = models.TextField(null=True, blank=True)
    pitscout_team = models.IntegerField(null=True, blank=True)

    team_number = models.IntegerField(max_length=5, verbose_name="Team Number")
    team_name = models.TextField(max_length=64, default=None, null=True, verbose_name="Team Name")
    team_website = models.TextField(max_length=128, default=None, null=True, verbose_name="Team Website")

    robot_height = models.FloatField(null=True, verbose_name="Robot Height")
    robot_weight = models.FloatField(null=True)
    robot_speed = models.FloatField(null=True)
    robot_wheel_count = models.IntegerField(null=True, max_length=2)
    can_strafe = models.NullBooleanField(null=True)
    

    driver_1 = models.TextField(max_length=64, default=None, null=True)
    driver_2 = models.TextField(max_length=64, default=None, null=True)
    coach = models.TextField(max_length=64, default=None, null=True)
    drive_coach_is_mentor = models.NullBooleanField(null=True)

    # autonomous
    can_reach_works = models.NullBooleanField(null=True)
    can_cross_works = models.NullBooleanField(null=True)
    can_score_boulders = models.NullBooleanField(null=True)
    auto_start_x = models.FloatField(null=True)
    auto_start_y = models.FloatField(null=True)

    # teleoperated
    can_score_high = models.NullBooleanField(null=True)
    can_score_low = models.NullBooleanField(null=True)
    can_cross_portcullis = models.NullBooleanField(null=True)
    can_cross_cheval = models.NullBooleanField(null=True)
    can_cross_moat = models.NullBooleanField(null=True)
    can_cross_ramparts = models.NullBooleanField(null=True)
    can_cross_drawbridge = models.NullBooleanField(null=True)
    can_cross_sally_port = models.NullBooleanField(null=True)
    can_cross_rock_wall = models.NullBooleanField(null=True)
    can_cross_rough_terrain = models.NullBooleanField(null=True)
    can_cross_low_bar = models.NullBooleanField(null=True)
    
    

    # other
    known_strengths = models.TextField(max_length=256, null=True)
    known_weaknesses = models.TextField(max_length=256, null=True)

    # image info (I have no idea how you do this ask terabyte)
    image_id = models.TextField(max_length=256, null=True, blank=True)
    image_link = models.TextField(max_length=256, null=True, blank=True)
    image_type = models.TextField(max_length=64, null=True, blank=True)

    def __str__(self):
        rt = self.scout.get_short_name() + " | " + str(self.location.name) + " | " + str(self.team_number)

        if self.scout.userprofile.team.team_number == self.team_number:
            rt += " (SELF)"

        return rt


class SitePreferences(models.Model):
    class Meta:
        verbose_name_plural = "Site preferences"

    site_url = models.TextField()
    login_message = models.TextField(blank=True, null=True)
    home_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.site_url
