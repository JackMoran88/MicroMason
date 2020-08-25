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
    context = {
        'categories': get_categories(),
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
