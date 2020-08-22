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
    sign_in = SingInForm(request.POST)

    if sign_in.is_valid():
        if sign_in_save(sign_in.cleaned_data):
            # redirect
            print("Success")
            sign_in_procedure(sign_in.cleaned_data, request)
            return redirect('/', request=request)
        else:
            # error
            print("Fail")
            return redirect('/', request=request)

    context = {
        'sign_in': sign_in
    }

    return render(request, 'basepage/sign_in.html', context=context)


"""
Main views
"""


def index(request):
    sing_in = SingInForm()

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


def sign_in_save(data_dictionary: dict) -> bool:
    try:
        user = Customer.objects.get(email=data_dictionary['email'])
    except Customer.DoesNotExist:
        return False

    if user.check_password(data_dictionary["password"]):
        return True


def sign_in_procedure(data_dictionary, request):
    user = Customer.objects.get(email=data_dictionary["email"])
    
