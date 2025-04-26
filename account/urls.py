from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
