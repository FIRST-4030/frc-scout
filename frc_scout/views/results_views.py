from django.contrib.auth.decorators import login_required
from django.shortcuts import render

__author__ = 'Sam'

def database_instructions(request):
    context = {
        'nav_title': "Connect to Database"
    }

    return render(request, 'frc_scout/results/connect_to_database.html', context)


@login_required
def average_scores(request):
    context = {
        'nav_title': "Average Scores"
    }

    return render(request, 'frc_scout/results/average_total_score.html', context)


def tableau_info(request):
    context = {
        'nav_title': "Integrating with Tableau",
    }

    return render(request, "frc_scout/results/tableau.html", context)