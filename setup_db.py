# NOTE: Only run this file once!
# This file will setup the database for initial use.
# Specifically, it will insert the default location names into the database
# so that people don't have to find them on their own every time.
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frc_scout_2015.settings")
import django
django.setup()

from frc_scout.models import Location
from frc_scout.views.loc_list import locations

if __name__ == "__main__":
    for loc_name in locations:
        new_loc = Location(name=loc_name)
        new_loc.save()
        print("Added location: " + loc_name)
