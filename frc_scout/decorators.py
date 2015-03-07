from django.http import HttpResponseRedirect
from frc_scout_2015 import local_settings


def secure_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request and not local_settings.SSL_LOGIN_DISABLED:
            if not request.is_secure():
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
            return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func


def insecure_required(view_func):
    def _wrapped_view_func(request, *args, **kwargs):
        if request and not local_settings.SSL_LOGIN_DISABLED:
            if request.is_secure():
                request_url = request.build_absolute_uri(request.get_full_path())
                insecure_url = request_url.replace('https://', 'http://')
                return HttpResponseRedirect(insecure_url)
            return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)
    return _wrapped_view_func