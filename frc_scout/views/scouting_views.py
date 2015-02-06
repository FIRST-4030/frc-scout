import json
from django.db.utils import IntegrityError
from django.shortcuts import render
from django.http import Http404, HttpResponse


# Match Scouting
from frc_scout.models import Match, Location, ToteStack, ContainerStack, PitScoutData


def match_scouting(request):

    context = {
        'fluid': True
    }

    return render(request, 'frc_scout/scouting/match/container.html', context)


def pit_scouting(request):

    context = {
        'fluid': False,
        'nav_title': "Pit Scouting"
    }

    return render(request, 'frc_scout/scouting/pit/container.html', context)


def submit_match_scouting_data(request):
    if request.method != "POST":
        raise Http404
    else:
        data = request.POST.get('data')

        matches = json.loads(data)

        errors = []

        for match in matches:

            if match:

                #
                # All variables that are NOT in separate database tables
                #

                location = Location.objects.get(id=request.session.get('location_id'))

                match_object = Match(scout=request.user, location=location)

                # PRE-MATCH
                if 'prematch' in match:
                    prematch = match['prematch']

                    for prematch_attr in prematch:
                        setattr(match_object, prematch_attr, prematch.get(prematch_attr))

                # AUTO START LOCATION
                if 'autonomous_starting_location' in match:
                    auto_starting_location = match['autonomous_starting_location']

                    for auto_start_attr in auto_starting_location:
                        setattr(match_object, auto_start_attr, auto_starting_location.get(auto_start_attr))

                # AUTONOMOUS
                if 'autonomous' in match:
                    auto = match['autonomous']

                    for auto_attr in auto:
                        setattr(match_object, auto_attr, auto.get(auto_attr))

                # AUTONOMOUS FOULS AND OTHER
                if 'autonomous_fouls_and_other' in match:
                    auto_fouls_other = match['autonomous_fouls_and_other']

                    for auto_fouls_other_attr in auto_fouls_other:
                        setattr(match_object, auto_fouls_other_attr, auto_fouls_other.get(auto_fouls_other_attr))

                # TELEOPERATED
                if 'teleoperated' in match:
                    tele = match['teleoperated']

                    for tele_attr in tele:
                        setattr(match_object, tele_attr, tele.get(tele_attr))

                # TELEOPERATED PICKED UP TOTES
                if 'teleoperated_picked_up_totes' in match:
                    tele_picked_up_totes = match['teleoperated_picked_up_totes']

                    for tele_picked_up_totes_attr in tele_picked_up_totes:
                        setattr(match_object, tele_picked_up_totes_attr, tele_picked_up_totes.get(tele_picked_up_totes_attr))

                # TELEOPERATED PICKED UP BINS
                if 'teleoperated_picked_up_containers' in match:
                    tele_picked_up_containers = match['teleoperated_picked_up_containers']

                    for tele_picked_up_containers_attr in tele_picked_up_containers:
                        setattr(match_object, tele_picked_up_containers_attr, tele_picked_up_containers.get(tele_picked_up_containers_attr))

                # TELEOPERATED FOULS AND OTHER
                if 'teleoperated_fouls_and_other' in match:
                    tele_fouls_other = match['teleoperated_fouls_and_other']

                    for tele_fouls_other_attr in tele_fouls_other:
                        setattr(match_object, tele_fouls_other_attr, tele_fouls_other.get(tele_fouls_other_attr))

                # POSTMATCH
                if 'postmatch' in match:
                    postmatch = match['postmatch']

                    for postmatch_attr in postmatch:
                        setattr(match_object, postmatch_attr, postmatch.get(postmatch_attr))

                try:
                    match_object.save()
                except IntegrityError:
                    errors.append({
                        'team_number': match['prematch']['team_number'],
                        'match_number': match['prematch']['match_number'],

                    })

                if 'teleoperated_stacked_totes' in match:
                    for stacked_totes in match['teleoperated_stacked_totes']:
                        tote_stack = ToteStack()

                        setattr(tote_stack, 'match', match_object)
                        setattr(tote_stack, 'start_height', stacked_totes['start_height'])
                        setattr(tote_stack, 'toted_added', stacked_totes['totes_added'])
                        setattr(tote_stack, 'x', stacked_totes['x'])
                        setattr(tote_stack, 'y', stacked_totes['y'])
                        setattr(tote_stack, 'coop_stack', stacked_totes['coop_stack'])

                        tote_stack.save()

                if 'teleoperated_stacked_containers' in match:
                    for stacked_containers in match['teleoperated_stacked_containers']:
                        bin_stack = ContainerStack()

                        setattr(bin_stack, 'match', match_object)
                        setattr(bin_stack, 'height', stacked_containers)
    
                        bin_stack.save()

        if len(errors) != 0:
            return HttpResponse(json.dumps(errors), status=200)
        else:
            return HttpResponse(status=200)


def submit_pit_scouting_data(request):
    if request.method != "POST":
        return HttpResponse(status=403)

    else:
        data = json.loads(request.POST.get('data'))

        data_object = PitScoutData(scout=request.user,
                                   location=Location.objects.get(id=request.session.get('location_id')))
        for name in data:
            setattr(data_object, name, data.get(name))

        data_object.save()

        return HttpResponse(status=200)
