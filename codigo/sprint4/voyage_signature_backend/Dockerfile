
# Use a imagem Alpine Linux como base
FROM python:3
EXPOSE 8000

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o código-fonte da sua aplicação para o contêiner
COPY . .

# Instale as dependências do seu aplicativo (se houver um arquivo requirements.txt)
RUN pip install -r requirements.txt

# Comando para executar sua aplicação (ajuste conforme necessário)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]