from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from frc_scout.models import Team, Match, Event
from frc_scout.decorators import insecure_required
from frc_scout.views.team_management_views import match_score
import json

__author__ = 'Sam'


def database_instructions(request):
    context = {
        'nav_title': "Connect to Database",
        'parent': reverse('frc_scout:index')
    }

    return render(request, 'frc_scout/results/connect_to_database.html', context)


@login_required
def average_scores(request):
    context = {
        'nav_title': "Average Scores"
    }

    return render(request, 'frc_scout/results/average_total_score.html', context)


def tableau_info(request):
    context = {
        'nav_title': "Integrating with Tableau",
        'parent': reverse('frc_scout:index')
    }

    return render(request, "frc_scout/results/tableau.html", context)

@insecure_required
def view_match_data(request):
    if not request.user.is_authenticated():
        return  HttpResponse(status=403)
    if request.method != "POST":
        return HttpResponseNotAllowed(["Post"])
    else:
        data = request.POST.get('data')
        
        params = json.loads(data)
        
        matches = Match.objects.filter(team_number=params.get("team")).exclude(location__name="TEST")
        if not params.get("god"):
            matches = matches.filter(scout__userprofile__team__team_number=request.user.userprofile.team.team_number)
        if params.get("this_location"):
            matches = matches.filter(location=request.session.get('location_id'))
        if params.get("filter"):
            matches.filter(**params.get("filter"))
        if params.get("order"):
            matches.order_by(params.get("order"))
        results = []
        for x in matches:
            events = Event.objects.filter(match=x)
            x.events = [y for y in events]
            results.append(x)
        return JsonResponse(results, safe=False)
def view_pit_data(request):
    if not request.user.is_authenticated():
        return  HttpResponse(status=403)
    if request.method != "POST":
        return HttpResponseNotAllowed(["Post"])
    else:
        data = request.POST.get('data')
        
        params = json.loads(data)
        
        matches = Match.objects.filter(team_number=params.get("team")).exclude(location__name="TEST")
        if not params.get("god"):
            matches = matches.filter(scout__userprofile__team__team_number=request.user.userprofile.team.team_number)
        