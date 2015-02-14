from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import Avg

from frc_scout.models import Match, Team, PitScoutData


@login_required
def view_team_profile(request, team_number=None):

    if not team_number:
        team_number = request.user.userprofile.team.team_number

    # oh boy here we go
    average_sections = {}
    matches = Match.objects.filter(team_number=team_number) # only take matches for this team
    # iterate over possible match fields
    for field in Match._meta.fields:
        # field_type = IntegerField, BooleanField, etc.
        field_type = str(field.__class__).split("'")[1].split('.')[4]
        # field_name = tele_picked_up_yellow_crates_blah, etc.
        field_name = str(field).split('.')[2]
        # field_section = either 'Teleoperated' or 'Autonomous'
        field_section = field_name.split("_")[0].capitalize()
        # fancy_field_name = the verbose name of the field
        fancy_field_name = field.verbose_name.capitalize()
        if field_section == "Tele":
            field_section = "Teleoperated"
        if field_section == "Auto":
            field_section = "Autonomous"
        if field_type == "IntegerField":
            # if it's an integer and not a special field
            if field_name != "team_number" and field_name != "match_number":
                # then calculate the average of it

                m = matches.aggregate(Avg(field_name))[field_name+"__avg"]

                if m is not None:
                    value = str("%.2f" % matches.aggregate(Avg(field_name))[field_name+"__avg"])
                else:
                    value = None
            else:
                # if it's special, skip it
                continue
        elif field_type == "BooleanField":
            # if it's a boolean, calculate the % that has true (but not if matches.count()  == 0)
            try:
                value = str("%.2f%%" % (matches.filter(**{str(field_name): True}).count() / matches.count() * 100))
            except ZeroDivisionError:
                pass
        else:
            # otherwise, skip it
            continue
        # if we haven't yet looked at the section that it's in...
        if field_section not in average_sections:
            # create a new entry for it (yes, this is redundant, we'll fix it later)
            average_sections[field_section] = {
                'name': field_section,
                'data': [],
            }
        # then, add the number into the data of the section entry
        average_sections[field_section]['data'].append({
            'name': fancy_field_name,
            'value': value,
        })

    pluralized = False

    try:
        team = Team.objects.get(team_number=team_number)
        team_name = team.team_name

        if str.endswith(team_name, "s"):
            pluralized = True

    except Team.DoesNotExist:
        team = None

    pit_scout_data = PitScoutData.objects.filter(team_number=team_number)



    # then pass all the sections/data to the context
    context = {
        'pluralized': pluralized,
        'team_number': team_number,
        # this converts e.g. {'auto': {'name':'auto', 'data':[{...}]}, ...}
        # to [{'name':'auto', 'data':[{...}]}, ...]
        # (this is necessary because otherwise the sections could show up in any order
        # when we iterate over the dictionary)
        'sections': [average_sections[z] for z in sorted(list(average_sections))],
        'team': team,
        'nav_title': str("%s's Profile" % team_number),
        'matches': matches
    }
    return render(request, 'frc_scout/view_team_profile.html', context)


def view_team_matches(request, team_number=None):
    context = {
        'team_number': team_number,
        'matches': Match.objects.filter(team_number=team_number),
        'nav_title': team_number + "'s Matches"
    }
    return render(request, 'frc_scout/view_team_matches.html', context)


def edit_team_profile(request):
    pass