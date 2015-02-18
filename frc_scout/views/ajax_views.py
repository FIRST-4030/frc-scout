import json
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Avg, Count
from django.http.response import HttpResponse
from frc_scout.models import Team, Location, Match
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
    location_list = {}
    for loc in Location.objects.all():
        location_list[loc.name] = loc.id

    return HttpResponse(json.dumps(location_list), content_type='application/json')


@login_required
def get_averages(request):

    matches = Match.objects.values('team_number').annotate(
        total_matches=Count('team_number'),
        auto_yellow_stacked_totes=Avg('auto_yellow_stacked_totes'),
        auto_yellow_moved_totes=Avg('auto_yellow_moved_totes'),
        auto_moved_to_auto_zone=Avg('auto_moved_to_auto_zone'),

        auto_moved_containers=Avg('auto_moved_containers'),

        tele_pushed_litter=Avg('tele_pushed_litter'),
        tele_placed_in_container_litter=Avg('tele_placed_in_container_litter'),

        totestack_start_height=Avg('totestack__start_height'),
        totestack_totes_added=Avg('totestack__totes_added'),

        number_of_totestacks=Count('totestack'),

        containerstack_height=Avg('containerstack__height'),

        number_of_containerstacks=Avg('containerstack'),
        ).filter(location__id=request.session.get('location_id'))

    processed_matches = []

    for match in matches:
        auto_score = 0

        # multiply by point value, divide by robots per alliance

        if match['auto_moved_to_auto_zone'] is not None:
            auto_score += (match['auto_moved_to_auto_zone'] / 3 * 4)

        if match['auto_moved_to_auto_zone'] is not None:
            auto_score += (match['auto_moved_to_auto_zone'] / 3 * 6)

        if match['auto_moved_to_auto_zone'] is not None:
            auto_score += (match['auto_moved_to_auto_zone'] / 3 * 20)

        tele_score = 0

        # worth 2 per tote stacked (average)
        if match['totestack_totes_added'] is not None:
            tele_score += match['totestack_totes_added'] * (match['number_of_totestacks'] / match['total_matches']) * 2

        if match['containerstack_height'] is not None:
            tele_score += match['containerstack_height'] * (match['number_of_containerstacks'] / match['total_matches']) * 4

        # processed_matches[match['team_number']] = {
        #     'auto_score': auto_score,
        #     'tele_score': tele_score
        # }

        processed_matches.append({
            'name': match['team_number'],

        })

    return HttpResponse(json.dumps(processed_matches))



    
    
    
    
    
    
    
    
    
    
    
    
    