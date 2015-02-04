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

        return HttpResponse(str("YIPPEE WE GOT SOME DATA! %i matches in fact" % len(parsed_data)))

