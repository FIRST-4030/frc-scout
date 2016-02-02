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
    url(r'^manage/find_match/$', views.find_match, name='find_match'),
    url(r'^manage/edit_match/(?P<match_id>[0-9]+)/$', views.edit_match, name='edit_match'),
    url(r'^manage/edit_match/update/$', views.edit_match_post, name='edit_match_post'),
    url(r'^manage/edit_match/delete/$', views.delete_match, name='delete_match'),

    # Account views
    url(r'^account/profile/$', views.update_profile, name='update_profile'),
    url(r'^account/password/$', views.update_password, name='update_password'),

    # Scouting views
    url(r'^scouting/match/$', views.match_scouting, name='match_scouting'),
    url(r'^scouting/match/practice/$', views.match_scouting_practice, name='match_scouting_practice'),
    url(r'^scouting/match/submit/$', views.submit_match_scouting_data, name='submit_match_scouting_data'),
    url(r'^scouting/pit/$', views.pit_scouting, name='pit_scouting'),
    url(r'^scouting/pit/submit/$', views.submit_pit_scouting_data, name='submit_pit_scouting_data'),

    # Profile views
    url(r'^team/$', views.view_team_profile, name='view_team_profile'),
    url(r'^team/(?P<team_number>-?[0-9]+)/$', views.view_team_profile, name='view_team_profile'),
    url(r'^team/(?P<team_number>-?[0-9]+)/pit/$', views.view_team_pit_data, name='view_team_pit_data'),

    url(r'^team/edit/$', views.edit_team_profiles, name='edit_team_profile'),


    # Results views
    url(r'^results/database/$', views.database_instructions, name='database_instructions'),
    url(r'^results/tableau/$', views.tableau_info, name='tableau_info'),

    # Event views
    url(r'^event/teams/$', views.teams_at_event, name='teams_at_event'),
    
    

    
    )
