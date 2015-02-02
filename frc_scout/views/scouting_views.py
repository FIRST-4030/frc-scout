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
        return HttpResponse(data)
