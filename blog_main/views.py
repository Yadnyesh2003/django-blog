from django.http import HttpResponse
from django.shortcuts import render, redirect
from blog_main.forms import RegistrationForm
from blogs.models import Blog, Category
from miscellaneous.models import About
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import auth
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.core.paginator import Paginator


def permission_denied_view(request, exception=None):
    return render(request, 'dashboard/permission_denied.html', status=403)

# def home(request):
#     # categories = Category.objects.all()
#     featured_posts = Blog.objects.filter(is_featured=True, status="Published").order_by('updated_at')
#     posts = Blog.objects.filter(is_featured=False, status="Published").order_by('updated_at')
#     try:
#         about = About.objects.get()
#     except:
#         about = None
#     context = {
#         # 'categories': categories,
#         'featured_posts': featured_posts,
#         'posts': posts,
#         'about': about,
#     }
#     return render(request, 'home.html', context)

def home(request):
    featured_queryset = Blog.objects.filter(is_featured=True, status="Published").order_by('updated_at')
    hero_post = None
    featured_stories_list = []
    
    if featured_queryset.exists():
        hero_post = featured_queryset[0]
        featured_stories_list = featured_queryset[1:]

    featured_paginator = Paginator(featured_stories_list, 4)
    featured_page_number = request.GET.get('featured_page')
    featured_posts = featured_paginator.get_page(featured_page_number)

    latest_queryset = Blog.objects.filter(is_featured=False, status="Published").order_by('updated_at')
    
    latest_paginator = Paginator(latest_queryset, 2)
    latest_page_number = request.GET.get('page')
    posts = latest_paginator.get_page(latest_page_number)

    try:
        about = About.objects.get()
    except:
        about = None

    context = {
        'hero_post': hero_post,
        'featured_posts': featured_posts,
        'posts': posts,
        'about': about,
    }
    return render(request, 'home.html', context)


def register(request):
    if(request.method == 'POST'):
        # pass
        form = RegistrationForm(request.POST)
        if(form.is_valid()):
            user = form.save()
            viewer_group = Group.objects.get(name='Viewer_Permissions')
            user.groups.add(viewer_group)
            return redirect('login')
            # HttpResponse("User registered successfully")
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'register.html', context)


# def login(request):
#     if(request.method == 'POST'):
#         form = AuthenticationForm(request, request.POST)
#         if(form.is_valid()):
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#         user = auth.authenticate(username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             if user.groups.filter(name='Viewer_Permissions').exists():
#                 return redirect('home')
#             elif (
#                 user.groups.filter(name__in=['Editor_Permissions', 'Manager_Permissions']).exists()
#                 or user.is_superuser
#             ):
#                 return redirect('dashboard')
#             else:
#                 return HttpResponse("No appropriate group assigned. Contact Admin.")
#         else:
#             print(form.errors)
#     form = AuthenticationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'login.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.groups.filter(name='Viewer_Permissions').exists():
                return redirect('home')
            elif (
                user.groups.filter(name__in=['Editor_Permissions', 'Manager_Permissions']).exists()
                or user.is_superuser
            ):
                return redirect('dashboard')
            else:
                messages.error(
                    request,
                    "Your account has no assigned permissions. Please contact the administrator."
                )
                logout(request)
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth.logout(request)
    return redirect('home')