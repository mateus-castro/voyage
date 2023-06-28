from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
from .classification import main

filepath = '../../sprint2/classification.py'

def hello_world(request):

    tree_accuracy, forest_accuracy = main()
    response = {
        "tree_accuracy" : tree_accuracy,
        "forest_accurracy" : forest_accuracy
    }

    return JsonResponse(response, status=200)