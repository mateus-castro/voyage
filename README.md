# voyage
<!-- 
oq fazer antes de rodar o .yaml:
	criar as chaves .pem com os nomes: "voyage-private.pem" e "voyage-public.pem"

etapas para realizar após o cloudformation:

adicionar os ips elásticos no security group privado -> só colocar o tipo de protocolo como TCP personalizado o id do sg como ip pra permissão

jogar a chave .pem privada pra todas as máquinas
scp -i <chave_pem_acesso>.pem ./<chave_envio>.pem ubuntu@<ip_instancia>:~

-->

# instruções para levantar o docker mongo
docker build -t voyage-db . # executar com os arquivos Dockerfile e mongodb.conf no diretório
docker run --name voyage-db -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=voyager -e MONGO_INITDB_ROOT_PASSWORD=dm95YWdlOnZveWFnZWFp voyage-db

# instruções para acessar o docker
mongo --username voyager --password dm95YWdlOnZveWFnZWFp --authenticationDataba admin --host 172.31.43.182 --port 27017

# mongo connection string
mongodb://voyager:dm95YWdlOnZveWFnZWFp@172.31.43.182:27017/voyage