from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, TemplateView
from .forms import UserForm, UserEditForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user_login = authenticate(username=user.username, password=form.cleaned_data['password'])

            if user_login is not None:
                login(request, user_login)
                return redirect('main:dashboard')
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})

class Profile(LoginRequiredMixin, TemplateView):
    template_name = 'account/profile.html'

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=request.user, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'account/profile_edit.html', {"form": form})