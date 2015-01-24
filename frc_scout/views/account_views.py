from django.contrib import messages
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


@login_required
def update_password(request):
    context = {
        'nav_title': "Update Password",
        'location': request.session.get('location')
    }

    if request.method == "POST":
        old_password = request.POST.get('old_password')
        password = request.POST.get('new_password')
        password_repeat = request.POST.get('new_password_repeat')

        if password != password_repeat:
            messages.error(request, "Your passwords did not match. Please try again.")
            return render(request, 'frc_scout/account/update_password.html', context)

        if not request.user.check_password(old_password):
            messages.error(request, "Your old password was entered incorrectly. Please try again.")
            return render(request, 'frc_scout/account/update_password.html', context)

        request.user.set_password(password)
        request.user.save()
        messages.success(request, "Password updated successfully.")

    return render(request, 'frc_scout/account/update_password.html', context)
