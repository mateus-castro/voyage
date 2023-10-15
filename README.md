# Voyage #
A Voyage é um algoritmo de reconhecimento de assinaturas de pintores do impressionismo com foco na diferenciação de imagens geradas por IAs generativas.

<!-- 
## setando ambiente
oq fazer antes de rodar o .yaml:
	criar as chaves .pem com os nomes: "voyage-private.pem" e "voyage-public.pem"

etapas para realizar após o cloudformation:

adicionar os ips elásticos no security group privado -> só colocar o tipo de protocolo como TCP personalizado o id do sg como ip pra permissão

jogar a chave .pem privada pra todas as máquinas
scp -i <chave_pem_acesso>.pem ./<chave_envio>.pem ubuntu@<ip_instancia>:~
-->

### instruções para levantar o docker mongo
	docker build -t voyage-db . # executar com os arquivos Dockerfile e mongodb.conf no diretório

	docker run --name voyage-db -d -p 27017:27017 -e MONGO_INITDB_ROOT_USERNAME=voyager -e MONGO_INITDB_ROOT_PASSWORD=dm95YWdlOnZveWFnZWFp voyage-db

### instruções para acessar o docker
mongo --username voyager --password dm95YWdlOnZveWFnZWFp --authenticationDataba admin --host 172.31.43.182 --port 27017

### mongo connection string
mongodb://voyager:dm95YWdlOnZveWFnZWFp@172.31.43.182:27017/voyage

# modelos de aprendizado de máquina
## descrição das variáveis utilizadas
vocab_size_percentage 	-> porcentagem de keypoints selecionados das imagens pra compor o vocabulário via Kmeans

test_size 		-> porcentagem da massa de testes para fit do modelo

n_neighbors 		-> número de neighbors pro KNN

### v1
	knn_model_accuracy - 0.78
	vocab_size_percentage=22
	test_size=0.18688722363757573
	n_neighbors=3

### v2
	knn_model_accuracy - 0.80
	vocab_size_percentage: 14
	test_size: 0.1814186208012823
	n_neighbors: 3

### cnn - proposta professor américo
	val_loss: 0.1494
	val_accuracy: 0.9318
