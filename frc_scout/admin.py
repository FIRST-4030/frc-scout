from django.contrib import admin

# Register your models here.
from frc_scout.models import UserProfile, Team, Location, Match, Event, PitScoutData, MatchPrivateComments, SitePreferences

admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Location)
admin.site.register(Match)
admin.site.register(Event)
admin.site.register(PitScoutData)
admin.site.register(MatchPrivateComments)
admin.site.register(SitePreferences)