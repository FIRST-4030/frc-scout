from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import render


@login_required
def view_scouts(request):
    if not request.user.userprofile.team_manager:
        raise Http404

    team = request.user.userprofile.team

    scouts = User.objects.filter(userprofile__team=team).exclude(id=request.user.id)

    context = {
        'location': request.session.get('location'),
        'scouts': scouts,
        'nav_title': 'Manage Scouts'
    }

    return render(request, 'frc_scout/manage/view_scouts.html', context)


@login_required
def update_scouts(request):
    if not request.user.userprofile.team_manager:
        raise Http404

    if request.method == "POST":
        pass