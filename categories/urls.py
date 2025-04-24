from django.urls import path
from . import views

app_name = 'categories'
urlpatterns = [
    path('add/', views.CategoryCreateView.as_view(), name='add_category'),
    path('delete/<int:category_id>/', views.category_delete, name='category_delete'),
    path('', views.CategoryListView.as_view(), name='category_list'),
]