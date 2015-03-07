__author__ = 'Sam'

APP_ID = "frc4030:frcscout.com:v1"


def make_tba_request(url_param):
    TBA_URL = "http://thebluealliance.com/api/v2/" + url_param

    TBA_URL += "?X-TBA-App-Id=" + APP_ID

