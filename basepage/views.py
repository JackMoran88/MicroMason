from django.shortcuts import render, redirect
from .models import Category, Customer
from .forms import SingInForm


""" 
API for Vue
"""


def base(request):
    return render(request, 'base.html')


def api_sign_up(request):
    return render(request, 'basepage/sign_up.html')


def api_sign_in(request):
    sing_in = SingInForm(request.POST)

    if sing_in.is_valid():
        if sing_in_save(sing_in.cleaned_data):
            # redirect
            print("Success")
            return redirect('/')
        else:
            # error
            print("Fail")
            return redirect('/')

    return render(request, 'basepage/sign_in.html')


"""
Main views
"""


def index(request):
    sing_in = SingInForm()

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
    parent_categories = Category.objects.filter(parent__isnull=True)

    for category in parent_categories:
        categories[category] = Category.objects.filter(parent__exact=category)

    return categories


def sing_in_save(data_dictionary: dict) -> bool:
    try:
        user = Customer.objects.get(email=data_dictionary['email'])
    except Customer.DoesNotExist:
        return False

    if user.check_password(data_dictionary["password"]):
        return True
