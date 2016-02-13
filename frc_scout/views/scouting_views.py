import json
from django.core.urlresolvers import reverse
from django.db.utils import IntegrityError, DataError
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
import decimal


# Match Scouting
from frc_scout.decorators import insecure_required
from frc_scout.models import Match, Location, PitScoutData, MatchPrivateComments, Event
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


def submit_match_scouting_data(request):
    if request.method != "POST":
        raise Http404
    else:
        data = str(request.POST.get('data'))
        matches = json.loads(data)
        
        eventsStorage = []
        
        errors = []

        for match in matches:

            if match:

                #
                # All variables that are NOT in separate database tables
                #

                if match['practice_scouting']:
                    try:
                        location = Location.objects.filter(name="TEST")[0]
                    except Location.DoesNotExist and IndexError:
                        Location(name="TEST").save()
                        location = Location.objects.filter(name="TEST")[0]

                else:
                    try:
                        location = Location.objects.get(id=request.session.get('location_id'))
                    except Location.DoesNotExist:
                        pass

                match_object = Match(scout=request.user,
                                     location=location,
                                     scout_name=request.user.first_name + " " + request.user.last_name[:1],
                                     scout_team_number=request.user.userprofile.team.team_number)

                # TELEOPERATED
                if match['events']:
                    events = match.pop('events')
                    
                    for x in range(len(events)):
                        event = events[x]
                        event_object = Event(ev_num=x,team_number=match['team_number'])
                        for event_attr in event:
                            setattr(event_object, event_attr, event.get(event_attr)) #todo: data validation. just in case.
                        eventsStorage.append(event_object)
                
                for attr in match:
                    setattr(match_object, attr, match.get(attr))
                print(str(match_object.__dict__))
                try:
                    match_object.save()
                    for event in eventsStorage:
                        event.match=match_object
                        event.save()
                except (IntegrityError, ValueError, DataError, decimal.InvalidOperation) as e:
                    try:
                        errors.append({
                            'team_number': match.get('prematch').get('team_number'),
                            'match_number': match.get('prematch').get('match_number'),
                            'error':str(e)
                            })
                    except AttributeError:
                        errors.append({
                            'team_number': "Unknown",
                            'match_number': "Unknown",
                            'error':str(e)
                        })
                

        if len(errors) != 0:
            return JsonResponse(errors, status=400, safe=False)
        else:
            return HttpResponse(status=200)


@insecure_required
def submit_pit_scouting_data(request):
    if request.method != "POST":
        return HttpResponse(status=403)

    else:
        data = json.loads(str(request.POST.get('data')))
        if request.POST.get('image_data'):
            image_data = json.loads(str(request.POST.get('image_data')))
        else:
            image_data = "nope"
        data_object = PitScoutData(scout=request.user,
                                   location=Location.objects.get(id=request.session.get('location_id')),
                                   pitscout_name=request.user.first_name + " " + request.user.last_name[:1],
                                   pitscout_team=request\
                                   .user\
                                   .userprofile\
                                   .team\
                                   .team_number)
        for name in data:
            setattr(data_object, name, data.get(name))

        if image_data != "nope":
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
