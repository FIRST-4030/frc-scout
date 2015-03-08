import json
from frc_scout.models import Location, PitScoutData
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse
from django.shortcuts import render
import requests


def teams_at_event(request):
    context = {
        'nav_title': "Teams Here",
        'parent': reverse('frc_scout:index')
    }
    try:
        location = Location.objects.get(id=request.session.get('location_id'))
    except Location.DoesNotExist:
        return HttpResponse("Your session does not have a location associated with it.", status=400)

    tba_url = str('http://www.thebluealliance.com/api/v2/event/2015%s/teams?X-TBA-App-Id=frc4030:frcscout.com:v1' % location.tba_event_code)

    try:
        r = requests.get(tba_url)
    except BaseException:
        return HttpResponse("Internet connection failed.")

    try:
        tba_teams = r.json()
    except ValueError:
        return HttpResponse("There is no event code for your location.", status=400)

    processed_teams = []
    try:
        all_pit_scout_data = PitScoutData.objects.filter(location=location)
    except PitScoutData.DoesNotExist:
        all_pit_scout_data = None

    for team in tba_teams:
        try:
            this_data = all_pit_scout_data.filter(team_number=team['team_number'])
            if len(this_data) > 0:
                scouted_here = True
            else:
                scouted_here = False
        except PitScoutData.DoesNotExist:
            this_data = None
            scouted_here = False


        processed_teams.append({
            'team_name': team['nickname'],
            'team_number': team['team_number'],
            'scouted_here': scouted_here,
            'data': this_data
        })

    context['teams'] = processed_teams

    return render(request, 'frc_scout/event/teams_at_event.html', context)