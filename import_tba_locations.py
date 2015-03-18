# The purpose of this file is to synchronize our locations with those on TBA,
# add IDs, and add any that are not already there

__author__ = 'Sam'

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frc_scout_2015.settings")
import django
import requests

django.setup()

from frc_scout.models import Location

APP_ID = "frc4030:frcscout.com:v1"

TBA_URL = "http://www.thebluealliance.com/api/v2/events/2015?X-TBA-App-Id=" + APP_ID

try:
    tba_locations = requests.get(TBA_URL).json()
except ValueError:
    print("Unable to parse JSON, check your URL.")
    exit(-1)

for tba_location in tba_locations:
    already_existed = False
    try:
        scout_location = Location.objects.get(name=tba_location['name'])
        already_existed = True
    except Location.DoesNotExist:
        scout_location = Location(name=tba_location['name'])

    print(str(scout_location) + " -- already existed in our db: " + str(already_existed) + " added code " + tba_location['event_code'])

    scout_location.tba_event_code = tba_location['event_code']
    scout_location.venue_address = tba_location['venue_address']
    scout_location.location = tba_location['location']

    scout_location.save()
