import json
from django.shortcuts import render
from django.http import Http404, HttpResponse

# Match Scouting
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

        parsed_data = json.loads(data)

        # prematch = parsed_data.prematch
        # autonomous_starting_location = parsed_data.autonomous_starting_location
        # autonomous = parsed_data.autonomous
        # teleoperated = parsed_data.teleoperated
        # postmatch = parsed_data.postmatch

        return HttpResponse(parsed_data)
