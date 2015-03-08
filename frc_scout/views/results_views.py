from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from frc_scout.models import Team, Match
from frc_scout.views.team_management_views import match_score

__author__ = 'Sam'


def database_instructions(request):
    context = {
        'nav_title': "Connect to Database",
        'parent': reverse('frc_scout:index')
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
        'parent': reverse('frc_scout:index')
    }

    return render(request, "frc_scout/results/tableau.html", context)


def view_team_averages(request, only_us, only_here):
    teams = Match.objects.values_list('team_number', flat=True).distinct()
    print(teams)
    scores = []
    for team_number in teams:
        total_auto = 0
        total_tele = 0

        matches = Match.objects.filter(team_number=team_number).exclude(location__name="TEST")
        if only_us:
            matches = matches.filter(scout__userprofile__team__team_number=request.user.userprofile.team.team_number)
        if only_here:
            matches = matches.filter(location=request.session.get('location_id'))

        for match in matches:
            auto_score, tele_score = match_score(match)
            total_auto += auto_score
            total_tele += tele_score
        try:
            avg_auto = total_auto / len(matches)
            avg_tele = total_tele / len(matches)
            avg_total = avg_auto + avg_tele

            avg_auto = str("%.2f" % avg_auto)
            avg_tele = str("%.2f" % avg_tele)
            avg_total = str("%.2f" % avg_total)

            scores.append({'team': team_number,
                'auto': avg_auto, 'tele': avg_tele, 'total': avg_total})

        except ZeroDivisionError:
            scores.append({'team': team_number,
                'auto': "—", 'tele': "—", 'total': "—"})

        scores = [s for s in scores if s['total'] != "—"]

    scores = sorted(scores, key=lambda k: 0 if k['total'] == "—" else float(k['total']), reverse=True)


    context = {
        'nav_title': "Team Averages",
        'parent': reverse('frc_scout:index'),
        'scores': scores,
        'opts': { 'only_us' : only_us, 'only_here' : only_here },
    }

    return render(request, "frc_scout/results/team_averages.html", context)
