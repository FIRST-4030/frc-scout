from django.contrib.auth import authenticate, logout, login
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib import messages


def index(request):
    if request.user.is_authenticated():
        return render(request, 'frc_scout/index.html')
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
                login(request, user)
                request.session['location'] = location
                return HttpResponseRedirect(reverse('frc_scout:index'))
            else:
                messages.error(request, "Your user has been disabled. Check with your team manager.")
        else:
            messages.error(request, "Your credentials did not match a user, try again.")

    return render(request, 'frc_scout/login.html')


# Cannot be named logout() because it conflicts with django internally and causes an infinite loop
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return HttpResponseRedirect(reverse('frc_scout:login'))