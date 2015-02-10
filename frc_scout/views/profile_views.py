from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import Avg

from frc_scout.models import Match

@login_required
def view_team_profile(request, team_number=None):
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
                value = matches.aggregate(Avg(field_name))[field_name+"__avg"]
            else:
                # if it's special, skip it
                continue
        elif field_type == "BooleanField":
            # if it's a boolean, calculate the % that has true
            value = str(matches.filter(**{str(field_name): True}).count() / matches.count() * 100) + "%"
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
    # then pass all the sections/data to the context
    context = {
        'team_number': team_number,
        # this converts e.g. {'auto': {'name':'auto', 'data':[{...}]}, ...}
        # to [{'name':'auto', 'data':[{...}]}, ...]
        # (this is necessary because otherwise the sections could show up in any order
        # when we iterate over the dictionary)
        'sections': [average_sections[z] for z in sorted(list(average_sections))]
    }
    return render(request, 'frc_scout/view_team_profile.html', context)

def view_team_matches(request, team_number=None):
    context = {
        'team_number': team_number,
        'matches': Match.objects.filter(team_number=team_number),
    }
    return render(request, 'frc_scout/view_team_matches.html', context)
