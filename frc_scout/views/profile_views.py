from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import Avg, Sum, Count
from frc_scout.decorators import insecure_required

from frc_scout.models import Match, Team, Event, PitScoutData
from frc_scout.tba_request import make_tba_request

__author__ = 'Miles'


@insecure_required
@login_required
def view_team_profile(request, team_number=None):

    if not team_number:
        team_number = request.user.userprofile.team.team_number

    elif int(team_number) < 1:
        return HttpResponse("Team numbers cannot be less than 1.", status=400)

    # oh boy here we go
    statistics = {}

    matches = Match.objects.filter(team_number=team_number).exclude(location__name="TEST") # only take matches for this team
    if matches is not None:
        # iterate over possible match fields
        for field in Match._meta.fields:
            value = None
            # field_type = IntegerField, BooleanField, etc.
            field_type = str(field.__class__).split("'")[1].split('.')[4]
            # field_name = tele_picked_up_yellow_crates_blah, etc.
            field_name = str(field).split('.')[2]
            if field_type == "IntegerField":
                # if it's an integer and not a special field
                if field_name != "team_number" and field_name != "match_number" and field_name != "scout_team_number":
                    # then calculate the average of it

                    m = matches.aggregate(Avg(field_name))[field_name+"__avg"]

                    if m is not None:
                        #value = str("%.2f" % matches.aggregate(Avg(field_name))[field_name+"__avg"])
                        value = str("%.2f" % matches.aggregate(Avg(field_name))[field_name+"__avg"])
                    else:
                        value = None
                else:
                    # if it's special, skip it
                    continue
            elif field_type == "BooleanField":
                # if it's a boolean, calculate the % that has true (but not if matches.count()  == 0)
                try:
                    value = str("%.2f" % (matches.filter(**{str(field_name): True}).count() / matches.count() * 100))
                except ZeroDivisionError:
                    pass
            else:
                # otherwise, skip it
                continue
            # put it in the hash -- much simpler than the crazy wacko system of before
            statistics[field_name] = value

            if statistics[field_name] == None:
                statistics[field_name] = "—"

    pit_scout_data = PitScoutData.objects.filter(team_number=team_number).order_by('id').exclude(location__name="TEST")

    aggregate_data = PitScoutData(team_number=team_number)

    for data in pit_scout_data:
        for field in PitScoutData._meta.fields:
            if getattr(data, field.name):
                setattr(aggregate_data, field.name, getattr(data, field.name))

    self_scouted = PitScoutData.objects.filter\
        (team_number=team_number, scout__userprofile__team__team_number=team_number).order_by('id')

    for data in self_scouted:
        for field in PitScoutData._meta.fields:
            if getattr(data, field.name):
                setattr(aggregate_data, field.name, getattr(data, field.name))

    # then pass all the sections/data to the context
    pitdatas = PitScoutData.objects.filter(team_number=team_number).count()

    try:
        param = str("team/frc%i" % int(team_number))
        json_decoded = make_tba_request(param)

    except ValueError:
        json_decoded = None

    context = {
        'has_pit_data': pitdatas,
        'aggregate_data': model_to_dict(aggregate_data),
        'team_number': team_number,
        'statistics': statistics,
        'nav_title': str(team_number),
        'matches': matches,
        'tba_data': json_decoded
    }
    if pitdatas == 1:
        context['scout_name'] = PitScoutData.objects.get(team_number=team_number).scout.first_name

    return render(request, 'frc_scout/profiles/profile.html', context)


@insecure_required
@login_required
def view_team_pit_data(request, team_number=None):
    context = {
        'nav_title': str(team_number) + "'s Pit Data",
        'team_number': team_number,
        'pit_data': sorted(PitScoutData.objects.filter(team_number=team_number), key=cmp_pit_data(request), reverse=True),
    }
    return render(request, 'frc_scout/profiles/pit_data.html', context)


@insecure_required
@login_required
def cmp_pit_data(request):
    def score_pit_data(pd):
        score = 0
        if pd.pitscout_team_number == pd.team_number:
            # self-scouting is worth 2 'points'
            score += 2
        if pd.pitscout_team_number == request.user.userprofile.team.team_number:
            # being scouted by your team is worth 1 'point'
            score += 1
        if pd.location.id == request.session.get('location_id'):
            # being at the same location is worth 4
            score += 4
        return score
    return score_pit_data

def edit_team_profiles(request):
    pass
