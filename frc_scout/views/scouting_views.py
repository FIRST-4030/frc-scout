import json
from django.shortcuts import render
from django.http import Http404, HttpResponse


# Match Scouting
from frc_scout.models import Match


def match_scouting(request):

    context = {
        'fluid': True
    }

    return render(request, 'frc_scout/scouting/match/container.html', context)


def submit_match_scouting_data(request):
    if request.method != "POST":
        raise Http404
    else:
        data = request.POST.get('data')

        matches = json.loads(data)

        for match in matches:
            prematch = match['prematch']

            match_object = Match()

            for prematch_attr in prematch:
                setattr(match_object, prematch_attr, prematch.get(prematch_attr))

            

