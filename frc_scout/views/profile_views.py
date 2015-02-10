from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import Avg

from frc_scout.models import Match

@login_required
def view_team_profile(request, team_number=None):
    average_sections = {}
    matches = Match.objects.filter(team_number=team_number)
    for field in Match._meta.fields:
        field_type = str(field.__class__).split("'")[1].split('.')[4]
        field_name = str(field).split('.')[2]
        field_section = field_name.split("_")[0].capitalize()
        fancy_field_name = field.verbose_name.capitalize()
        if field_section == "Tele":
            field_section = "Teleoperated"
        if field_section == "Auto":
            field_section = "Autonomous"
        if field_type == "IntegerField":
            if field_name != "team_number" and field_name != "match_number":
                value = matches.aggregate(Avg(field_name))[field_name+"__avg"]
            else:
                continue
        elif field_type == "BooleanField":
            value = str(matches.filter(**{str(field_name): True}).count() / matches.count() * 100) + "%"
        else:
            print(field_type)
            continue
        print(field_type + "!")
        if field_section not in average_sections:
            average_sections[field_section] = {
                'name': field_section,
                'data': [],
            }
        average_sections[field_section]['data'].append({
            'name': fancy_field_name,
            'value': value,
        })
    context = {
        'team_number': team_number,
        'sections': [average_sections[z] for z in sorted(list(average_sections))]
    }
    return render(request, 'frc_scout/view_team_profile.html', context)

def view_team_matches(request, team_number=None):
    context = {
        'team_number': team_number,
        'matches': Match.objects.filter(team_number=team_number),
    }
    return render(request, 'frc_scout/view_team_matches.html', context)
