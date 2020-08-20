from django.shortcuts import render
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
    return render(request, 'basepage/sign_in.html')


"""
Main views
"""


def index(request):
    if request.method == 'POST':
        form = SingInForm(request.POST)

        if form.is_valid():
            if sing_in_save(form.cleaned_data):
                # redirect
                pass
            else:
                # error
                pass
    else:
        form = SingInForm()

    context = {
        'categories': get_categories(),
        'form': form,
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
