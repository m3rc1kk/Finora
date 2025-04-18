from django.contrib.auth import authenticate, login
from django.shortcuts import render

from .forms import UserForm


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_login = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

            if user_login is None:
                login(request, user_login)
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})