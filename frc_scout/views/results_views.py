from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from frc_scout.models import Team, Match, Event, PitScoutData
from frc_scout.decorators import insecure_required
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
def view_team_match_data(request):
    if not request.user.is_authenticated():
        return  HttpResponse(status=403)
    if request.method != "POST":
        return HttpResponseNotAllowed(["Post"])
    else:
        data = request.POST.get('data')
        
        params = json.loads(data)
        
        if not params.get("team"):
            return HttpResponse('{"error":"missing team number"', status=400)
        
        matches = Match.objects.filter(team_number=params.get("team")).exclude(location__name="TEST")
        if not params.get("god"):
            matches = matches.filter(scout__userprofile__team__team_number=request.user.userprofile.team.team_number)
        if params.get("this_location"):
            matches = matches.filter(location=request.session.get('location_id'))
        if params.get("filter"):
            matches.filter(**params.get("filter"))
        if params.get("order"):
            matches.order_by(params.get("order"))
        if params.get("columns"):
            results = [x for x in matches.values(params.get("columns"))]
        else:
            results = [x for x in matches.values()]
        return JsonResponse(results, safe=False)
@insecure_required
def view_event_data(request):
    if not request.user.is_authenticated():
        return  HttpResponse(status=403)
    if request.method != "POST":
        return HttpResponseNotAllowed(["Post"])
    else:
        data = request.POST.get('data')
        params = json.loads(data)
        if not params.get("match"):
            return HttpResponse('{"error":"missing match number"', status=400)
        events = Event.objects.filter(match_id=params.get("match")).order_by("time").values()
        results = [x for x in events]
        return JsonResponse(results, safe=False)
@insecure_required
def view_team_event_data(request):
    if not request.user.is_authenticated():
        return  HttpResponse(status=403)
    if request.method != "POST":
        return HttpResponseNotAllowed(["Post"])
    else:
        data = request.POST.get('data')
        params = json.loads(data)
        if not params.get("team"):
            return HttpResponse('{"error":"missing team number"', status=400)
        events = Event.objects.filter(team_number=params.get("team"))
        if params.get("filter"):
            events.filter(**params.get("filter"))
        if params.get("order"):
            events.order_by(params.get("order"))
        if params.get("columns"):
            results = [x for x in events.values(params.get("columns"))]
        else:
            results = [x for x in events.values()]
    return JsonResponse(results, safe=False)
        
def view_pit_data(request):
    if not request.user.is_authenticated():
        return  HttpResponse(status=403)
    if request.method != "POST":
        return HttpResponseNotAllowed(["Post"])
    else:
        data = request.POST.get('data')
        
        params = json.loads(data)
        
        pit = PitScoutData.objects.filter(team_number=params.get("team"))
        if not params.get("god"):
            pit = pit.filter(scout__userprofile__team__team_number=request.user.userprofile.team.team_number)
        if params.get("this_location"):
            pit = pit.filter(location=request.session.get('location_id'))
        if params.get("columns"):
            results = [x for x in pit.values(params.get("columns"))]
        else:
            results = [x for x in pit.values()]
    return JsonResponse(results, safe=False)