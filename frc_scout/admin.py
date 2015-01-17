from django.contrib import admin

# Register your models here.
from frc_scout.models import UserProfile, Team

admin.site.register(UserProfile)
admin.site.register(Team)