from django.contrib import admin

# Register your models here.
from frc_scout.models import UserProfile, Team, Location

admin.site.register(UserProfile)
admin.site.register(Team)
admin.site.register(Location)
