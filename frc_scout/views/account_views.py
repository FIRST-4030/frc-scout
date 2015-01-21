from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def update_profile(request):
    if request.method == "POST":
        pass
    else:
        context = {
            'nav_title': "Update Profile",
            'location': request.session.get('location')
        }
        return render(request, 'frc_scout/account/update_profile.html', context)