from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
from .main_model import Processador
# from .main_disponib import main_disp

processador = Processador()

def backend_show_model(request):

    knn_model_accuracy, vocab_size_percentage, test_size, n_neighbors = processador.show_model()
    # main_info = main()
    
    response = {
        # "model_training_info" : model_info
        "knn_model_accuracy": knn_model_accuracy,
        "vocab_size_percentage": vocab_size_percentage,
        "test_size": test_size,
        "n_neighbors": n_neighbors
    }

    return JsonResponse(response, status=200)

def backend_disponib(request):
    disponib = main()
    response = {
        "disponib" : disponib
    }

    return JsonResponse(response, status=200)

    