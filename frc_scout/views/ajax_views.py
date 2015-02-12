import json
from django.contrib.auth.decorators import login_required
from django.db.models.aggregates import Avg
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
        auto_yellow_stacked_totes=Avg('auto_yellow_stacked_totes'),
        auto_yellow_moved_totes=Avg('auto_yellow_moved_totes'),
        auto_grey_acquired_totes=Avg('auto_grey_acquired_totes'),
        auto_step_center_acquired_containers=Avg('auto_step_center_acquired_containers'),
        auto_ground_acquired_containers=Avg('auto_ground_acquired_containers'),
        auto_moved_containers=Avg('auto_moved_containers'),

        tele_picked_up_ground_upright_totes=Avg('tele_picked_up_ground_upright_totes'),
        tele_picked_up_upside_down_totes=Avg('tele_picked_up_upside_down_totes'),
        tele_picked_up_sideways_totes=Avg('tele_picked_up_sideways_totes'),
        tele_picked_up_human_station_totes=Avg('tele_picked_up_human_station_totes'),
        tele_picked_up_sideways_containers=Avg('tele_picked_up_sideways_containers'),
        tele_picked_up_upright_containers=Avg('tele_picked_up_upright_containers'),
        tele_picked_up_center_step_containers=Avg('tele_picked_up_center_step_containers'),
        tele_pushed_litter=Avg('tele_pushed_litter'),
        tele_placed_in_container_litter=Avg('tele_placed_in_container_litter'),
        tele_fouls=Avg('tele_fouls'),

        tele_knocked_over_stacks=Avg('tele_knocked_over_stacks'),
        totestack_start_height=Avg('totestack__start_height'),
        totestack_totes_added=Avg('totestack__totes_added'),
        containerstack_height=Avg('containerstack__height'),
        )

    return HttpResponse(json.dumps(list(matches)))


    
    
    
    
    
    
    
    
    
    
    
    
    