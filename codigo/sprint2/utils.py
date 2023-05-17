import os
import glob
import json

diretorio_principal = "images/"

# Obter os nomes dos subdiretórios
subdiretorios = [diretorio for diretorio in os.listdir(diretorio_principal) if os.path.isdir(os.path.join(diretorio_principal, diretorio))]

# Criar um dicionário para armazenar os dados JSON em cada subdiretório
dicionario_de_listas = {}
for subdiretorio in subdiretorios:
    caminho_subdiretorio = os.path.join(diretorio_principal, subdiretorio)
    arquivos_json = glob.glob(os.path.join(caminho_subdiretorio, "*.json"))
    
    lista_arquivos = []
    for arquivo_json in arquivos_json:
        with open(arquivo_json, 'r') as arquivo:
            dados_json = json.load(arquivo)
            lista_arquivos.append(dados_json)
    
    dicionario_de_listas[subdiretorio] = lista_arquivos

# Exemplo de uso: Iterar sobre os dados JSON em cada subdiretório
for subdiretorio, lista in dicionario_de_listas.items():
    for dados_json in lista:
        # Faça algo com os dados JSON
        print(f"No subdiretório {subdiretorio}: {dados_json}")
print(lista_arquivos)