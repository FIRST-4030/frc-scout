__author__ = 'Sam'

from django.conf.urls import patterns, url

from frc_scout import views

urlpatterns = patterns(
    '',

    # About us
    url(r'^about/$', views.about, name='about_us'),

    # Views dealing with session stuff stored in session_views.py
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^create/$', views.create_account, name='create_account'),

    # JSON calls
    url(r'^json/team_exists/$', views.check_if_team_exists, name='check_if_team_exists'),
    url(r'^json/username_exists/$', views.check_if_username_exists, name='check_if_username_exists'),
    url(r'^json/locations/$', views.get_locations, name='get_locations'),
    url(r'^json/results/averages/$', views.get_averages, name='get_averages'),

    # Team management views
    url(r'^manage/scouts/$', views.view_scouts, name='view_scouts'),
    url(r'^manage/scouts/update/$', views.update_scouts, name='update_scouts'),

    # Account views
    url(r'^account/profile/$', views.update_profile, name='update_profile'),
    url(r'^account/password/$', views.update_password, name='update_password'),

    # Scouting views
    url(r'^scouting/match/$', views.match_scouting, name='match_scouting'),
    url(r'^scouting/match/submit/$', views.submit_match_scouting_data, name='submit_match_scouting_data'),
    url(r'^scouting/pit/$', views.pit_scouting, name='pit_scouting'),
    url(r'^scouting/pit/submit/$', views.submit_pit_scouting_data, name='submit_pit_scouting_data'),

    # Profile views
    url(r'^team/$', views.view_team_profile, name='view_team_profile'),
    url(r'^team/(?P<team_number>[0-9]+)/$', views.view_team_profile, name='view_team_profile'),

    url(r'^team/edit/$', views.edit_team_profile, name='edit_team_profile'),

    url(r'^team/(?P<team_number>[0-9]+)/matches/$', views.view_team_matches, name='view_team_matches'),

    # Results views
    url(r'^results/database/$', views.database_instructions, name='database_instructions'),
    url(r'^results/tableau/$', views.tableau_info, name='tableau_info'),
    #url(r'^results/averages/$', views.average_scores, name='average_scores'),

)
