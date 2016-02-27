from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Avg, Count, Sum
from django.forms.models import model_to_dict
from django.http.response import Http404, HttpResponse
from django.shortcuts import render
from frc_scout.models import Location, Match, Event


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
        'parent': reverse('frc_scout:index'),
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

MAX_RESULTS = 100

@login_required
def find_match(request):

    context = {
        'nav_title': "Find Match",
        'locations': Location.objects.all().order_by('name'),
        'parent': reverse('frc_scout:index')
    }

    if request.GET:
        scouting_team = request.GET.get('scouting_team', None)
        team_number = request.GET.get('team_number', None)
        match_number = request.GET.get('match_number', None)
        location_id = request.GET.get('location', None)

        matches = Match.objects.filter(location__id=location_id).order_by('-match_number')

        if request.user.is_superuser:
            if scouting_team and scouting_team != "":
                matches = matches.filter(scout__userprofile__team__team_number=scouting_team)

        elif request.user.userprofile.team_manager:
            matches = matches.filter(scout__userprofile__team__team_number=request.user.userprofile.team.team_number)

        else:
            matches = matches.filter(scout=request.user)

        if team_number and team_number != "":
            matches = matches.filter(team_number=team_number)

        if match_number and match_number != "":
            matches = matches.filter(match_number=match_number)

        processed_matches = []

        if matches.count() > MAX_RESULTS:
            context['truncated'] = True
        else:
            context['truncated'] = False

        matches = matches[:MAX_RESULTS]

        for match in matches:

            processed_matches.append({
                'scout': match.scout,
                'team_number': match.team_number,
                'id': match.id,
                'match_number': match.match_number,
                'timestamp': match.timestamp,
                })

        context['matches'] = processed_matches

    return render(request, 'frc_scout/manage/find_match.html', context)



@login_required
def delete_match(request):
    match_id = request.POST.get('match_id', None)

    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        raise Http404

    # need to be manager (or needs to be their data)

    if not request.user.is_superuser:
        if not request.user.userprofile.team_manager and match.scout != request.user:
            return HttpResponse(status=403)

    # needs to be their data
    if match.scout.userprofile.team.team_number != request.user.userprofile.team.team_number:
        return HttpResponse(status=403)

    match.delete()
    return HttpResponse(status=200)


@login_required
def edit_match(request, match_id=None):
    try:
        match = Match.objects.get(id=match_id)
    except Match.DoesNotExist:
        raise Http404

    # need to be manager (or needs to be their data)

    if not request.user.is_superuser:
        if not request.user.userprofile.team_manager and match.scout != request.user:
            return HttpResponse(status=403)

    context = {
        'nav_title': "Edit Match",
        'match': match,
        'totestacks': match.totestack_set
    }

    return render(request, 'frc_scout/manage/edit_match.html', context)


def edit_match_post(request):
    if request.method != "POST":
        return HttpResponse(status=400)

    if request.POST.get('editable', False):
        name = request.POST.get('name')
        pk = request.POST.get('pk')

        if request.POST.get('match', False):
            try:
                match = Match.objects.get(id=pk)

            except Match.DoesNotExist:
                return HttpResponse(status=400)

                # need to be manager (or needs to be their data)

            if not request.user.is_superuser:
                if not request.user.userprofile.team_manager and match.scout != request.user:
                    return HttpResponse(status=403)

            if not request.POST.get('boolean', False):
                value = request.POST.get('value')
                setattr(match, name, value)

            else:
                current = model_to_dict(match)[name]
                setattr(match, name, not current)

            try:
                match.save()
            except ValueError:
                return HttpResponse("Field cannot be blank.", status=400)

        elif request.POST.get('totestack', False):
            try:
                totestack = ToteStack.objects.get(id=pk)

            except ToteStack.DoesNotExist:
                return HttpResponse(status=400)

            if not request.user.is_superuser:
                if not request.user.userprofile.team_manager and totestack.match.scout != request.user:
                    return HttpResponse(status=403)

            if not request.POST.get('boolean', False):
                value = request.POST.get('value')
                setattr(totestack, name, value)

            else:
                current = model_to_dict(totestack)[name]
                setattr(totestack, name, not current)

            try:
                totestack.save()
            except ValueError:
                return HttpResponse("Field cannot be blank.", status=400)

        elif request.POST.get('containerstack', False):
            try:
                containerstack = ContainerStack.objects.get(id=pk)

            except ToteStack.DoesNotExist:
                return HttpResponse(status=400)

            if not request.user.is_superuser:
                if not request.user.userprofile.team_manager and containerstack.match.scout != request.user:
                    return HttpResponse(status=403)

            if not request.POST.get('boolean', False):
                value = request.POST.get('value')
                setattr(containerstack, name, value)

            else:
                current = model_to_dict(containerstack)[name]
                setattr(containerstack, name, not current)

            try:
                containerstack.save()
            except ValueError:
                return HttpResponse("Field cannot be blank.", status=400)

        return HttpResponse(status=200)

    elif request.POST.get('totestack_location', False):
        id = request.POST.get('id', None)

        try:
            totestack = ToteStack.objects.get(id=id)

        except ToteStack.DoesNotExist:
            return HttpResponse(status=400)

        if not request.user.is_superuser:
            if not request.user.userprofile.team_manager and totestack.match.scout != request.user:
                return HttpResponse(status=403)

        try:
            totestack.x = request.POST.get('x')
            totestack.y = request.POST.get('y')
            totestack.save()
        except ValueError:
            return HttpResponse("Field cannot be blank.", status=400)

        return HttpResponse("success!", status=200)

    else:
        return HttpResponse(status=400)
