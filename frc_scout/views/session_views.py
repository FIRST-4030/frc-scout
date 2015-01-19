from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from frc_scout.models import Team, UserProfile
from django.db import IntegrityError

from frc_scout.views.loc_list import locations


def index(request):
    if request.user.is_authenticated():
        context = {
            'user': request.user,
            'nav_title': "Home",
            'location': request.session.get('location')
        }
        return render(request, 'frc_scout/index.html', context)
    else:
        return HttpResponseRedirect(reverse('frc_scout:login'))


# Cannot be named login() because it conflicts with django internally and causes an infinite loop
def login_view(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('frc_scout:index'))

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        location = request.POST.get('location')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                if location in locations:
                    login(request, user)

                    request.session['location'] = location

                    return HttpResponseRedirect(reverse('frc_scout:index'))
                else:
                    messages.error(request, "Please enter a valid event location.")
            else:
                messages.error(request, "Your account has been disabled (or has not yet been enabled). Check with your team manager.")
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

        user.userprofile.team, created = Team.objects.get_or_create(team_number=team_number, id=team_number)

        # If the team is newly created, the user is the manager
        if created:
            user.userprofile.team_manager = True
            user.userprofile.approved = True

        # Otherwise, they must be approved
        else:
            user.is_active = False

        user.userprofile.save()

        messages.success(request, "Account created successfully, you may now login.")
        return HttpResponseRedirect(reverse("frc_scout:login"))

    return render(request, 'frc_scout/create_account.html')
