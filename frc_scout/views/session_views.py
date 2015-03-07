import json

from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from frc_scout.models import Team, UserProfile, Location, SitePreferences, Match
from django.db import IntegrityError
from frc_scout.decorators import secure_required, insecure_required
from frc_scout_2015 import local_settings


@insecure_required
def index(request):
    if request.user.is_authenticated():
        context = {
            'user': request.user,
            'nav_title': "Home",
            'no_back': True,
            'location_id': request.session.get('location_id'),
            'location_name': request.session.get('location_name'),
            }

        try:
            location = Location.objects.get(id=request.session.get('location_id'))
            event_code = location.tba_event_code

            context['event_code'] = event_code
        except Location.DoesNotExist:
            pass

        try:
            obj = SitePreferences.objects.filter(site_url=local_settings.SITE_URL)
            if obj:
                context['home_messages'] = obj[0].home_message

        except SitePreferences.DoesNotExist:
            pass

        return render(request, 'frc_scout/index.html', context)
    else:
        return HttpResponseRedirect(reverse('frc_scout:login'))


@secure_required
# Cannot be named login() because it conflicts with django internally and causes an infinite loop
def login_view(request):

    location_list = {}
    for loc in Location.objects.all():
        location_list[loc.name] = loc.id

    context = {
        'location_list': json.dumps(location_list),
        'total_teams': Team.objects.all().count(),
        'total_matches': Match.objects.all().values('location', 'match_number').exclude(location__name="TEST").count(),
        'total_users': User.objects.all().count()
        }

    try:
        obj = SitePreferences.objects.filter(site_url=local_settings.SITE_URL)
        if obj:
            context['login_message'] = obj[0].login_message

    except SitePreferences.DoesNotExist:
        pass

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('frc_scout:index'))

    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            location_name = request.POST.get('location')

            user = authenticate(username=username, password=password)

            if user is None:
                try:
                    email = User.objects.get(email=username)

                    user = authenticate(username=email.username, password=password)
                except User.DoesNotExist:
                    user = None

            location = Location.objects.get(name=location_name).id

            if user is not None:
                if user.is_active and user.userprofile.approved:
                    login(request, user)

                    request.session['location_name'] = location_name
                    request.session['location_id'] = location

                    return HttpResponseRedirect(reverse('frc_scout:index'))
                else:
                    messages.error(request, "Your account has been disabled "
                                            "(or has not yet been enabled). Check with your team manager.")
            else:
                messages.error(request, "Your credentials did not match a user, try again.")

    except Location.DoesNotExist:
        messages.error(request, "Please enter a valid event location.")

    return render(request, 'frc_scout/login.html', context)


# Cannot be named logout(), see above
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return HttpResponseRedirect(reverse('frc_scout:login'))


@secure_required
def create_account(request):
    if request.method == "POST":
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Your passwords did not match.")
            return render(request, 'frc_scout/create_account.html')

        team_number = request.POST.get('team_number')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email_address = request.POST.get('email')

        team_manager_request = request.POST.get('request_team_manager', False)

        try:
            user = User.objects.create_user(username, email_address, password, first_name=first_name, last_name=last_name)
        except IntegrityError as e:
            messages.error(request, "That username (or email address) has been taken.")
            return render(request, 'frc_scout/create_account.html')

        user.userprofile = UserProfile()

        user.userprofile.team, created = Team.objects.get_or_create(team_number=team_number)

        # If the team is newly created, the user is the manager
        if created:
            user.userprofile.team_manager = True
            user.userprofile.approved = True

        user.userprofile.save()

        if not created and local_settings.SERVER_EMAIL is not None:
            team_managers = \
                User.objects.filter(userprofile__team__team_number=team_number, userprofile__team_manager=True).values('email')

            email_body = "Greetings,\n\n" \
                         "A new user, " + user.get_full_name() + ", has registered on FRC Scout under your team.\n" \
                         "To approve this user, go to: http://frcscout.com/manage/scouts/\n"

            manager_emails = []
            for m in team_managers:
                manager_emails.append(m['email'])

            if team_manager_request:
                email_body += \
                    "This user also requested to be made a team manager - you may promote them using the same link.\n"

            email_body += "\nSincerely,\n" \
                          "Scout Bot\n\n" \
                          "Generated " + str(timezone.now())

            send_mail("New user on FRC Scout", email_body, local_settings.SERVER_EMAIL, manager_emails)

        if created:
            messages.success(request, "Account created successfully, you may now login.")
        else:
            messages.info(request,
                          "Your account has been created, but must be approved by a team manager before you may login.")
        return HttpResponseRedirect(reverse("frc_scout:login"))

    return render(request, 'frc_scout/create_account.html')


def about(request):
    context = {
        'nav_title': "About FRC Scout",
    }

    return render(request, "frc_scout/about_frc_scout.html", context)