from django.shortcuts import render
from .models import Category


""" 
API for Vue
"""


def base(request):
    return render(request, 'base.html')


def api_sign_up(request):
    return render(request, 'basepage/sign_up.html')


def api_sign_in(request):
    return render(request, 'basepage/sign_in.html')


"""
Main views
"""


def index(request):
    return render(request, "basepage/index.html", {'categories': get_categories()})


"""
Support functions
"""


def get_categories():
    categories = {}
    parent_categories = Category.objects.filter(parent__isnull=True)

    for category in parent_categories:
        categories[category] = Category.objects.filter(parent__exact=category)

    return categories
