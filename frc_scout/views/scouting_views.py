from django.shortcuts import render


# For testing views
def get_view(request):
    name = request.GET.get('page')

    context = {
        'fluid': True
    }

    return render(request, 'frc_scout/scouting/' + name, context)


# Match Scouting
def match_scouting(request):

    context = {
        'fluid': True
    }

    return render(request, 'frc_scout/scouting/match/container.html', context)

