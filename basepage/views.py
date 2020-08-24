from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Category
from .forms import SingInForm


""" 
API for Vue
"""


def base(request):
    return render(request, 'base.html')


def api_sign_up(request):
    return render(request, 'basepage/sign_up.html')


def api_sign_in(request):
    sign_in = SingInForm(request.POST)

    if sign_in.is_valid():
        sign_in_procedure(sign_in.cleaned_data, request)

    context = {
        'sign_in': sign_in
    }

    return render(request, 'basepage/sign_in.html', context=context)


"""
Main views
"""


def index(request):
    sing_in = SingInForm()

    if request.user.is_authenticated:
        logout(request)
    print(request.user)

    context = {
        'categories': get_categories(),
        'sing_in': sing_in,
    }

    return render(request, "basepage/index.html", context=context)


"""
Support functions
"""


def get_categories():
    categories = {}
    grandparent_categories = Category.objects.filter(parent__isnull=True)

    for category in grandparent_categories:
        categories[category] = {}
        parents = Category.objects.filter(parent__exact=category)

        for parent in parents:
            children = Category.objects.filter(parent__exact=parent)
            categories[category][parent] = children

    return categories


def sign_in_procedure(data_dictionary: dict, request):
    user = authenticate(
        request,
        email=data_dictionary["email"],
        password=data_dictionary["password"]
    )

    if user:
        login(request, user)
        # ToDo special flags
        return redirect('/')
    else:
        # ToDo Error
        return redirect('/')

