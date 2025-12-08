from os import stat
from webbrowser import get
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from blogs.models import Blog, Category

# Create your views here.
def posts_by_category(request, category_id):
    # Fetch the posts that belong to the category with the id `category_id`
    posts = Blog.objects.filter(status="Published", category=category_id).order_by('updated_at')
    # try:
    #     category = Category.objects.get(pk=category_id)
    # except:
    #     return redirect('home')
    category = get_object_or_404(Category, pk=category_id)
    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'posts_by_category.html', context)