from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render


@login_required
def update_profile(request):
    if request.method == "POST":
        pk = request.POST.get('pk')
        value = request.POST.get('value')

        user = request.user
        setattr(user, pk, value)
        user.save()

        return HttpResponse(status=200)

    else:
        context = {
            'nav_title': "Update Profile",
            'location': request.session.get('location')
        }
        return render(request, 'frc_scout/account/update_profile.html', context)

