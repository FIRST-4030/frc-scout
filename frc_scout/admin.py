from django.contrib import admin

# Register your models here.
from frc_scout.models import UserProfile, Team, Location, Match, ToteStack, BinStack

admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Location)
admin.site.register(Match)
admin.site.register(ToteStack)
admin.site.register(BinStack)