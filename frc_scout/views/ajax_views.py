import json
from django.http.response import HttpResponse
from frc_scout.models import Team, Location
from django.contrib.auth.models import User


def check_if_team_exists(request):
    team_exists = False

    if request.method == "POST":
        team_number = request.POST.get('team_number')
        if team_number is not None:
            try:
                team = Team.objects.get(team_number=team_number)
                team_exists = True
            except Exception:
                pass

    response = {
        'team_exists': team_exists
    }

    return HttpResponse(json.dumps(response), content_type='application/json')


def check_if_username_exists(request):
    username_exists = False

    if request.method == "POST":
        username = request.POST.get('username')
        if username is not None:
            try:
                user = User.objects.get(username=username)
                username_exists = True
            except Exception:
                pass

    response = {
        'username_exists': username_exists,
        'username': username
    }

    return HttpResponse(json.dumps(response), content_type='application/json')


def get_locations(request):
    location_list = []
    for loc in Location.objects.all():
        location_list.append("({'location': %s})" % loc.name)

    return HttpResponse(json.dumps(location_list), content_type='application/json')
