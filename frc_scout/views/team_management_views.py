from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from frc_scout.models import Location, Match


@login_required
def view_scouts(request):
    if not request.user.userprofile.team_manager:
        return HttpResponse(status=403)

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
        return HttpResponse(status=403)

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


@login_required
def find_match(request):
    if not request.user.userprofile.team_manager:
        return HttpResponse(status=403)
    context = {
        'nav_title': "Find Match",
        'locations': Location.objects.all().order_by('name')
    }

    if request.GET:
        team_number = request.GET.get('team_number', None)
        match_number = request.GET.get('match_number', None)
        location_id = request.GET.get('location', None)

        if match_number is not None and match_number != "":
            matches = Match.objects.filter(scout__userprofile__team__team_number=request.user.userprofile.team.team_number,
                                           team_number=team_number, match_number=match_number, location__id=location_id)
        else:
            matches = Match.objects.filter(scout__userprofile__team__team_number=request.user.userprofile.team.team_number,
                                           team_number=team_number, location__id=location_id)

        context['matches'] = matches

    return render(request, 'frc_scout/manage/find_match.html', context)