from django.contrib.auth.decorators import login_required
from django.shortcuts import render

__author__ = 'Sam'

@login_required
def database_instructions(request):
    context = {
        'nav_title': "Connect to Database"
    }
    return render(request, 'frc_scout/results/connect_to_database.html', context)