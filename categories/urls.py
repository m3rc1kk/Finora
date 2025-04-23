from django.urls import path
from . import views

app_name = 'categories'
urlpatterns = [
    path('add/', views.add_category, name='add_category'),
    path('delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('', views.category_list, name='category_list'),
]