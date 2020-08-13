from django.shortcuts import render
from .models import Category


def base(request):
    return render(request, 'base.html')


def index(request):
    categories = Category.objects.all()
    return render(request, "basepage/index.html", {'categories':categories})




def api_sign_up(request):
    return render(request, 'basepage/sign_up.html')

def api_sign_in(request):
    return render(request, 'basepage/sign_in.html')