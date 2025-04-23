from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm
from .models import Category


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

def category_list(request):
    categories = Category.objects.filter(user = request.user)
    system_categories = Category.objects.filter(is_system = True)
    return render(request, 'categories/categories_list.html', {"categories": categories, 'system_categories': system_categories})

def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id, user = request.user)
    if category.is_system:
        return redirect('categories:categories_list')
    category.delete()
    return redirect('categories:category_list')