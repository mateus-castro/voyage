from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
from .main_model import main
from .main_disponib import main_disp

def backend_show_model(request):

    model_info = main()
    response = {
        "model_training_info" : model_info
    }

    return JsonResponse(response, status=200)

def backend_disponib(request):
    disponib = main()
    response = {
        "disponib" : disponib
    }

    return JsonResponse(response, status=200)

    