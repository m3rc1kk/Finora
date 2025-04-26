from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import CategoryForm
from .models import Category


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('category_list')
    template_name = 'categories/add_category.html'
    def post(self, request, *args, **kwargs):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('categories:category_list')
        else:
            form = CategoryForm()
        return render(request, 'categories/add_category.html', {"form": form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            return redirect('categories:category_list')
    else:
        form = CategoryForm()

    return render(request, 'categories/add_category.html', {"form": form})

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'categories/categories_list.html'

    def get_context_data(self, **kwargs):

        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(user = self.request.user)
        context['system_categories'] = Category.objects.filter(is_system=True)

        return context



def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id, user = request.user)
    if category.is_system:
        return redirect('categories:categories_list')
    category.delete()
    return redirect('categories:category_list')