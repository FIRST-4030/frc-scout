__author__ = 'Sam'

from django.conf.urls import patterns, url

from frc_scout import views

urlpatterns = patterns(
    '',

    # Views dealing with session stuff stored in session_views.py
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^create/$', views.create_account, name='create_account'),

    # JSON calls
    url(r'^json/team_exists/$', views.check_if_team_exists, name='check_if_team_exists'),
    url(r'^json/username_exists/$', views.check_if_username_exists, name='check_if_username_exists'),
    url(r'^json/locations/$', views.get_locations, name='get_locations'),

    # Team management views
    url(r'^manage/scouts/$', views.view_scouts, name='view_scouts'),
    url(r'^manage/scouts/update/$', views.update_scouts, name='update_scouts'),

    # Account views
    url(r'^account/profile/$', views.update_profile, name='update_profile'),
    url(r'^account/password/$', views.update_password, name='update_password'),

    # FOR TESTING
    url(r'^view/$', views.get_view, name='get_view'),

    # Scouting views
    url(r'^scouting/match/$', views.match_scouting, name='match_scouting'),
)