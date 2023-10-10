from django.shortcuts import render
import json

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
    resposta = "Erro desconhecido"

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid() or True:
            print("arquivo recebido!")
            arquivo = request.FILES["imagem"]
            arquivoLido = arquivo.read()
            print("arquivo lido!")
    
            resultado_processamento = processador.processar(arquivoLido)
            response = {
                "origem_humana": bool(resultado_processamento[0])
            }

            return JsonResponse(response, status=200)
        else:
            resposta = "Formulário inválido!"
    else:
        resposta = "Método do request não POST"

    return JsonResponse({"resposta": resposta}, status=400)

from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()