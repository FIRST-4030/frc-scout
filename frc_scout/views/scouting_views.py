import json
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError, DataError
from django.shortcuts import render
from django.http import Http404, HttpResponse


# Match Scouting
from frc_scout.decorators import insecure_required
from frc_scout.models import Match, Location, ToteStack, ContainerStack, PitScoutData, MatchPrivateComments
from frc_scout.tba_request import make_tba_request
import requests

@insecure_required
def match_scouting(request):

    context = {
        'fluid': True,
        }

    return render(request, 'frc_scout/scouting/match/container.html', context)

@insecure_required
def match_scouting_practice(request):

    context = {
        'fluid': True,
        'practice_scouting': True,
        }

    return render(request, 'frc_scout/scouting/match/container.html', context)


@insecure_required
def pit_scouting(request):

    context = {
        'fluid': False,
        'nav_title': "Pit Scouting",
        'parent': reverse('frc_scout:index')
    }

    return render(request, 'frc_scout/scouting/pit/container.html', context)


@insecure_required
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

                if match['postmatch'].get('practice_scouting'):
                    try:
                        location = Location.objects.filter(name="TEST")[0]
                    except Location.DoesNotExist and IndexError:
                        Location(name="TEST").save()
                        location = Location.objects.filter(name="TEST")[0]

                else:
                    try:
                        location = Location.objects.get(id=request.session.get('location_id'))
                    except location.DoesNotExist:
                        pass

                match_object = Match(scout=request.user,
                                     location=location,
                                     scout_name=request.user.first_name + " " + request.user.last_name[:1],
                                     scout_team_number=request.user.userprofile.team.team_number)

                # PRE-MATCH
                if match.get('prematch'):
                    prematch = match.get('prematch')

                    for prematch_attr in prematch:
                        setattr(match_object, prematch_attr, prematch.get(prematch_attr))
                        print(prematch_attr)

                # AUTO START LOCATION
                if match.get('autonomous_starting_location'):
                    auto_starting_location = match.get('autonomous_starting_location')

                    for auto_start_attr in auto_starting_location:
                        setattr(match_object, auto_start_attr, auto_starting_location.get(auto_start_attr))

                # AUTONOMOUS
                if match.get('autonomous'):
                    auto = match.get('autonomous')

                    for auto_attr in auto:
                        setattr(match_object, auto_attr, auto.get(auto_attr))

                # AUTONOMOUS FOULS AND OTHER
                if match.get('autonomous_fouls_and_other'):
                    auto_fouls_other = match.get('autonomous_fouls_and_other')

                    for auto_fouls_other_attr in auto_fouls_other:
                        setattr(match_object, auto_fouls_other_attr, auto_fouls_other.get(auto_fouls_other_attr))

                # TELEOPERATED
                if match.get('teleoperated'):
                    tele = match.get('teleoperated')

                    for tele_attr in tele:
                        setattr(match_object, tele_attr, tele.get(tele_attr))

                # TELEOPERATED PICKED UP TOTES
                if match.get('teleoperated_picked_up_totes'):
                    tele_picked_up_totes = match.get('teleoperated_picked_up_totes')

                    for tele_picked_up_totes_attr in tele_picked_up_totes:
                        setattr(match_object, tele_picked_up_totes_attr, tele_picked_up_totes.get(tele_picked_up_totes_attr))

                # TELEOPERATED PICKED UP BINS
                if 'teleoperated_picked_up_containers' in match:
                    tele_picked_up_containers = match['teleoperated_picked_up_containers']

                    for tele_picked_up_containers_attr in tele_picked_up_containers:
                        setattr(match_object, tele_picked_up_containers_attr, tele_picked_up_containers.get(tele_picked_up_containers_attr))

                # TELEOPERATED FOULS AND OTHER
                if match.get('teleoperated_fouls_and_other'):
                    tele_fouls_other = match.get('teleoperated_fouls_and_other')

                    for tele_fouls_other_attr in tele_fouls_other:
                        setattr(match_object, tele_fouls_other_attr, tele_fouls_other.get(tele_fouls_other_attr))

                pc = MatchPrivateComments()
                # POSTMATCH
                if match.get('postmatch'):
                    postmatch = match.get('postmatch')

                    for postmatch_attr in postmatch:
                        setattr(match_object, postmatch_attr, postmatch.get(postmatch_attr))

                    # private comments
                    pc.comments = postmatch.get('tele_private_comments', None)
                try:
                    match_object.save()
                    pc.match = match_object
                    pc.save()
                except (IntegrityError, ValueError, DataError):
                    try:
                        errors.append({
                            'team_number': match.get('prematch').get('team_number'),
                            'match_number': match.get('prematch').get('match_number'),
                            })
                    except AttributeError:
                        errors.append({
                            'team_number': "Unknown",
                            'match_number': "Unknown",
                        })

                if match.get('teleoperated_stacked_totes'):
                    for stacked_totes in match.get('teleoperated_stacked_totes'):
                        tote_stack = ToteStack()

                        try:
                            setattr(tote_stack, 'match', match_object)
                            setattr(tote_stack, 'start_height', stacked_totes.get('start_height'))
                            setattr(tote_stack, 'totes_added', stacked_totes.get('totes_added'))
                            setattr(tote_stack, 'x', stacked_totes.get('x'))
                            setattr(tote_stack, 'y', stacked_totes.get('y'))
                            setattr(tote_stack, 'coop_stack', stacked_totes.get('coop_stack'))
                        except KeyError:
                            pass

                        try:
                            tote_stack.save()
                        except IntegrityError:
                            pass

                if match.get('teleoperated_stacked_containers'):
                    for stacked_containers in match.get('teleoperated_stacked_containers'):
                        bin_stack = ContainerStack()

                        setattr(bin_stack, 'match', match_object)
                        setattr(bin_stack, 'height', stacked_containers)

                        try:
                            bin_stack.save()
                        except IntegrityError:
                            pass

        if len(errors) != 0:
            return HttpResponse(json.dumps(errors), status=200)
        else:
            return HttpResponse(status=200)


@insecure_required
def submit_pit_scouting_data(request):
    if request.method != "POST":
        return HttpResponse(status=403)

    else:
        data = json.loads(request.POST.get('data'))
        image_data = json.loads(request.POST.get('image_data'))

        data_object = PitScoutData(scout=request.user,
                                   location=Location.objects.get(id=request.session.get('location_id')),
                                   pitscout_name=request.user.first_name + " " + request.user.last_name[:1],
                                   pitscout_team_number=request.user.userprofile.team.team_number)
        for name in data:
            setattr(data_object, name, data.get(name))

        if image_data.get('data'):
            data_object.image_id = image_data['data']['id']
            data_object.image_link = image_data['data']['link']
            data_object.image_type = image_data['data']['type']

        try:
            param = str("team/frc%i" % data.get('team_number'))

            json_decoded = make_tba_request(param)

            setattr(data_object, 'team_name', json_decoded.get('nickname'))
            setattr(data_object, 'team_website', json_decoded.get('website'))

        except ValueError:
            pass

        try:
            data_object.save()
        except (ValueError, IntegrityError):
            return HttpResponse(status=400)

        return HttpResponse(status=200)