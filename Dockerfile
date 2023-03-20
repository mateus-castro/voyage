# Usar a imagem base do Ubuntu 20.04
FROM ubuntu:20.04

# Instalar as atualizações mais recentes e as ferramentas necessárias
RUN apt-get update && apt-get -y upgrade && apt-get -y install gnupg wget

# Importar a chave pública do MongoDB
RUN wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | apt-key add -

# Adicionar o repositório do MongoDB ao APT
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-5.0.list

# Instalar o MongoDB
RUN apt-get update && apt-get -y install mongodb-org

# Copiar os arquivos de configuração personalizados
COPY mongodb.conf /etc/mongodb.conf

# Abrir a porta padrão do MongoDB
EXPOSE 27017

# Iniciar o servidor MongoDB
CMD ["mongod", "--config", "/etc/mongodb.conf"]

# Instalar o cliente do mongo pra poder acessá-lo
# RUN apt-get update && apt-get -y install mongodb-clients