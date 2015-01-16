from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from frc_scout.forms import LoginForm

__author__ = 'Sam'


def index(request):
    if request.user.is_authenticated():
        return render(request, 'frc_scout/index.html')
    else:
        if request.method == "POST":
            pass
        else:
            return HttpResponseRedirect(reverse('frc_scout:login'))


def login(request):
    context = {
        'form': LoginForm()
    }
    return render(request, 'frc_scout/login.html', context)