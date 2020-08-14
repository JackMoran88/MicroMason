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
    context = {'parent_categories': (parents := get_parent_categories()),
               'subcatgories': get_second_categories(parents)}

    print(context)

    return render(request, "basepage/index.html", context=context)


"""
Support functions
"""


def get_parent_categories():
    return Category.objects.filter(parent__isnull=True)


def get_second_categories(parents: list):
    categories = []
    for category in parents:
        categories.append(Category.objects.filter(parent__exact=category))

    return categories
