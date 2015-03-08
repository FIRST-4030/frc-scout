from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db.models import Avg, Sum
from frc_scout.decorators import insecure_required

from frc_scout.models import Match, Team, ToteStack, ContainerStack, PitScoutData
from frc_scout.views.team_management_views import match_score

__author__ = 'Miles'


@insecure_required
@login_required
def view_team_profile(request, team_number=None):

    if not team_number:
        team_number = request.user.userprofile.team.team_number

    elif int(team_number) < 1:
        return HttpResponse("Team numbers cannot be less than 1.", status=400)

    # oh boy here we go
    statistics = {}

    matches = Match.objects.filter(team_number=team_number).exclude(location__name="TEST") # only take matches for this team
    if matches is not None:
        # iterate over possible match fields
        for field in Match._meta.fields:
            value = None
            # field_type = IntegerField, BooleanField, etc.
            field_type = str(field.__class__).split("'")[1].split('.')[4]
            # field_name = tele_picked_up_yellow_crates_blah, etc.
            field_name = str(field).split('.')[2]
            if field_type == "IntegerField":
                # if it's an integer and not a special field
                if field_name != "team_number" and field_name != "match_number" and field_name != "scout_team_number":
                    # then calculate the average of it

                    m = matches.aggregate(Avg(field_name))[field_name+"__avg"]

                    if m is not None:
                        #value = str("%.2f" % matches.aggregate(Avg(field_name))[field_name+"__avg"])
                        value = str("%.2f" % matches.aggregate(Avg(field_name))[field_name+"__avg"])
                    else:
                        value = None
                else:
                    # if it's special, skip it
                    continue
            elif field_type == "BooleanField":
                # if it's a boolean, calculate the % that has true (but not if matches.count()  == 0)
                try:
                    value = str("%.2f" % (matches.filter(**{str(field_name): True}).count() / matches.count() * 100))
                except ZeroDivisionError:
                    pass
            else:
                # otherwise, skip it
                continue
            # put it in the hash -- much simpler than the crazy wacko system of before
            statistics[field_name] = value

            if statistics[field_name] == None:
                statistics[field_name] = "—"

        # calculate some special stats
        print(statistics['auto_step_center_acquired_containers'])
        if (statistics['auto_step_center_acquired_containers'] != "—") and (statistics['auto_ground_acquired_containers'] != "—"):
            statistics['auto_total_acquired_containers'] = str("%.2f" %
                (float(statistics['auto_step_center_acquired_containers']) + float(statistics['auto_ground_acquired_containers'])))
        else:
            statistics['auto_total_acquired_containers'] = "—"
        if (statistics['tele_picked_up_ground_upright_totes'] != "—") and (statistics['tele_picked_up_upside_down_totes'] != "—") and (
            statistics['tele_picked_up_sideways_totes'] != "—") and (statistics['tele_picked_up_human_station_totes'] != "—"):
            statistics['tele_picked_up_total_totes'] = str("%.2f" %
                (float(statistics['tele_picked_up_ground_upright_totes']) + float(statistics['tele_picked_up_upside_down_totes'])
                 + float(statistics['tele_picked_up_sideways_totes']) + float(statistics['tele_picked_up_human_station_totes'])))
        else:
            statistics['tele_picked_up_total_totes'] = "—"
        if (statistics['tele_picked_up_sideways_containers'] != "—") and (statistics['tele_picked_up_upright_containers'] != "—") and (
            statistics['tele_picked_up_center_step_containers'] != "—"):
            statistics['tele_picked_up_total_containers'] = str("%.2f" %
                 (float(statistics['tele_picked_up_sideways_containers']) + float(statistics['tele_picked_up_upright_containers'])
                 + float(statistics['tele_picked_up_center_step_containers'])))
        else:
            statistics['tele_picked_up_total_containers'] = "—"
        # aggregate totestacks, yay!
        stacks = ToteStack.objects.filter(match__team_number=team_number)
        if (len(stacks) != 0) and (stacks != "—"):
            statistics['tele_average_stack_height'] = str("%.2f" % stacks.aggregate(Avg('start_height'))['start_height__avg'])
            statistics['tele_average_totes_stacked'] = str("%.2f" % stacks.aggregate(Avg('totes_added'))['totes_added__avg'])
            # I'm pretty proud of this -- it's the averages of the sum per match
            match_stacks = stacks.values('match').annotate(total_totes=Sum('totes_added'))
            statistics['tele_average_totes_stacked_per_match'] = str("%.2f" % match_stacks.aggregate(Avg('total_totes'))['total_totes__avg'])
        else:
            statistics['tele_average_stack_height'] = "—"
            statistics['tele_average_totes_stacked'] = "—"
            statistics['tele_average_totes_stacked_per_match'] = "—"

        # match scores -- I moved the thing from the 'edit match' screen into its own function
        # because it's pretty useful and recyclable
        match_scores = [match_score(m) for m in matches]
        auto_scores = [m[0] for m in match_scores]
        tele_scores = [m[1] for m in match_scores]
        if len(auto_scores) > 0:
            statistics['auto_average_score'] = str("%.2f" % (sum(auto_scores) / len(auto_scores)))
            statistics['tele_average_score'] = str("%.2f" % (sum(tele_scores) / len(tele_scores)))
            statistics['total_average_score'] = str("%.2f" %
                (float(statistics['auto_average_score']) + float(statistics['tele_average_score'])))
        else:
            statistics['auto_average_score'] = "—"
            statistics['tele_average_score'] = "—"
            statistics['total_average_score'] = "—"
        if statistics['match_final_score'] != "—":
            try:
                statistics['total_score_proportion'] = str("%.2f" %
                    (float(statistics['total_average_score']) / float(statistics['match_final_score']) * 100))
            except ZeroDivisionError:
                statistics['total_score_proportion'] = "?"
        else:
            statistics['total_score_proportion'] = "—"

    pit_scout_data = PitScoutData.objects.filter(team_number=team_number).order_by('id').exclude(location__name="TEST")

    aggregate_data = PitScoutData(team_number=team_number)

    for data in pit_scout_data:
        for field in PitScoutData._meta.fields:
            if getattr(data, field.name):
                setattr(aggregate_data, field.name, getattr(data, field.name))

    self_scouted = PitScoutData.objects.filter\
        (team_number=team_number, scout__userprofile__team__team_number=team_number).order_by('id')

    for data in self_scouted:
        for field in PitScoutData._meta.fields:
            if getattr(data, field.name):
                setattr(aggregate_data, field.name, getattr(data, field.name))

    # then pass all the sections/data to the context
    context = {
        'aggregate_data': model_to_dict(aggregate_data),
        'team_number': team_number,
        'statistics': statistics,
        'nav_title': str(team_number),
        'matches': matches
    }
    return render(request, 'frc_scout/view_team_profile.html', context)


def view_team_matches(request, team_number=None):
    matches = []

    for match in Match.objects.filter(team_number=team_number).exclude(location__name="TEST").order_by('-timestamp'):
        match_dict = model_to_dict(match)

        if not match_dict['no_show']:
            match_dict['auto_total_score'], match_dict['tele_total_score'] = match_score(match)
            match_dict['total_score'] = match_dict['auto_total_score'] + match_dict['tele_total_score']
            match_dict['auto_total_score'] = str("%.2f" % match_dict['auto_total_score'])
            match_dict['tele_total_score'] = str("%.2f" % match_dict['tele_total_score'])
            if match_dict['match_final_score'] is not None:
                try:
                    match_dict['score_proportion'] = str("%.2f" % (match_dict['total_score'] / match_dict['match_final_score'] * 100))
                except ZeroDivisionError:
                    match_dict['score_proportion'] = "?"
            else:
                match_dict['score_proportion'] = "?"
            match_dict['total_score'] = str("%.2f" % match_dict['total_score'])

            stacks = ToteStack.objects.filter(match=match)
            if len(stacks) > 0:
                match_dict['tele_total_stacked'] = stacks.aggregate(Sum('totes_added'))['totes_added__sum']
                match_dict['tele_average_totes_stacked'] = str("%.2f" % stacks.aggregate(Avg('totes_added'))['totes_added__avg'])
                match_dict['tele_average_stack_height'] = str("%.2f" % stacks.aggregate(Avg('start_height'))['start_height__avg'])
            else:
                match_dict['tele_total_stacked'] = 0
                match_dict['tele_average_totes_stacked'] = "0.00"
                match_dict['tele_average_stack_height'] = "0.00"

            match_dict['tele_picked_up_total_containers'] = (match_dict['tele_picked_up_sideways_containers']
                + match_dict['tele_picked_up_upright_containers'] + match_dict['tele_picked_up_center_step_containers'])
            match_dict['auto_total_acquired_containers'] = (match_dict['auto_step_center_acquired_containers']
                + match_dict['auto_ground_acquired_containers'])
            match_dict['tele_picked_up_total_totes'] = (match_dict['tele_picked_up_ground_upright_totes']
                + match_dict['tele_picked_up_sideways_totes'] + match_dict['tele_picked_up_upside_down_totes']
                + match_dict['tele_picked_up_human_station_totes'])

            match_dict['auto_has_auto'] = not match_dict['auto_no_auto']

            for key in match_dict:
                if key == "no_show":
                    continue
                if str(match_dict[key]) == "True":
                    match_dict[key] = "Yes"
                if str(match_dict[key]) == "False":
                    match_dict[key] = "No"

        if match.scout.userprofile.team.team_number == request.user.userprofile.team.team_number:
            match_dict['match_private_comments'] = match.matchprivatecomments.comments
            match_dict['scout_name'] = match.scout.first_name + " on team " + str(match.scout.userprofile.team.team_number)
            match_dict['scout_first_name'] = match.scout.first_name
        else:
            match_dict['scout_name'] = 'team ' + str(match.scout.userprofile.team.team_number)

        match_dict['location'] = match.location.name

        matches.append(match_dict)

    context = {
        'team_number': team_number,
        'matches': matches,
        'nav_title': team_number + "'s Matches"
    }
    return render(request, 'frc_scout/view_team_matches.html', context)


def edit_team_profile(request):
    pass
