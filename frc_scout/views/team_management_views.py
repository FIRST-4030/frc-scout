from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from django.utils import timezone


@login_required
def view_scouts(request):
    if not request.user.userprofile.team_manager:
        raise Http404

    team = request.user.userprofile.team

    scouts = User.objects.filter(userprofile__team=team).exclude(id=request.user.id)

    unapproved_scouts = User.objects \
        .filter(userprofile__team=team, userprofile__approved=False) \
        .exclude(id=request.user.id)

    context = {
        'location': request.session.get('location'),
        'scouts': scouts,
        'nav_title': 'Manage Scouts',
        'unapproved_scouts': unapproved_scouts
    }

    return render(request, 'frc_scout/manage/view_scouts.html', context)



@login_required
def update_scouts(request):
    if not request.user.userprofile.team_manager:
        raise Http404

    if request.method == "POST":

        if 'scout_id' in request.POST:

            print('if')

            scout_id = request.POST.get('scout_id')
            action = request.POST.get('action')

            scout = User.objects.get(id=scout_id)

            if action == "team_manager":
                scout.userprofile.team_manager = not scout.userprofile.team_manager

            elif action == "approved":
                scout.userprofile.approved = not scout.userprofile.approved

            elif action == "banned":
                scout.userprofile.banned = not scout.userprofile.banned

            scout.userprofile.save()

        elif 'pk' in request.POST:

            pk = request.POST.get('pk')
            name = request.POST.get('name')
            value = request.POST.get('value')

            scout = User.objects.get(id=pk)

            setattr(scout.userprofile, name, value)

            scout.userprofile.save()

        return HttpResponse(status=200)

    raise Http404