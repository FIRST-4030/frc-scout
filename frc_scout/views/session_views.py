import json
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from frc_scout.models import Team, UserProfile, Location, SitePreferences
from django.db import IntegrityError
from frc_scout_2015 import local_settings

from frc_scout.views.loc_list import locations


def index(request):
    if request.user.is_authenticated():
        context = {
            'user': request.user,
            'nav_title': "Home",
            'location_id': request.session.get('location'),
            'location_name': request.session.get('location_name'),
            }

        try:
            obj = SitePreferences.objects.filter(site_url=local_settings.SITE_URL)
            if obj:
                context['home_messages'] = obj[0].home_message

        except SitePreferences.DoesNotExist:
            pass

        return render(request, 'frc_scout/index.html', context)
    else:
        return HttpResponseRedirect(reverse('frc_scout:login'))


# Cannot be named login() because it conflicts with django internally and causes an infinite loop
def login_view(request):

    location_list = {}
    for loc in Location.objects.all():
        location_list[loc.name] = loc.id

    context = {
        'location_list': json.dumps(location_list),
        }

    try:
        obj = SitePreferences.objects.filter(site_url=local_settings.SITE_URL)
        if obj:
            context['login_messages'] = obj[0].login_message

    except SitePreferences.DoesNotExist:
        pass

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('frc_scout:index'))

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

        if user is not None:
            if user.is_active:
                if location_name in locations:

                    location = Location.objects.get(name=location_name)

                    login(request, user)

                    request.session['location_name'] = location.name
                    request.session['location_id'] = location.id

                    return HttpResponseRedirect(reverse('frc_scout:index'))
                else:
                    messages.error(request, "Please enter a valid event location.")
            else:
                messages.error(request, "Your account has been disabled. Check with your team manager.")
        else:
            messages.error(request, "Your credentials did not match a user, try again.")

    return render(request, 'frc_scout/login.html')


# Cannot be named logout(), see above
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return HttpResponseRedirect(reverse('frc_scout:login'))


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

        try:
            user = User.objects.create_user(username, email_address, password, first_name=first_name, last_name=last_name)
        except IntegrityError:
            messages.error(request, "That username has been taken.")
            return render(request, 'frc_scout/create_account.html')

        user.userprofile = UserProfile()

        user.userprofile.team, created = Team.objects.get_or_create(team_number=team_number)

        # If the team is newly created, the user is the manager
        if created:
            user.userprofile.team_manager = True
            user.userprofile.approved = True

        user.userprofile.save()

        messages.success(request, "Account created successfully, you may now login.")
        return HttpResponseRedirect(reverse("frc_scout:login"))

    return render(request, 'frc_scout/create_account.html')
