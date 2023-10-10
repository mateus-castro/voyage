from django.shortcuts import render
import json

from django.http import HttpResponse
from django.http import JsonResponse
from .main_model import Processador

processador = Processador()

def backend_show_model(request):    
    response = {processador.show_model()}

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

            response = {"origem_ia": processador.processar(arquivoLido)}

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