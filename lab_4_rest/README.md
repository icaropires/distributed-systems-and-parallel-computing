## Instalação
### Pré requisitos
* docker
* docker-compose
* python3

### instalação das outras dependências do projeto
* Na pasta master e repository execute o comando `sudo docker-compose build`
* Na pasta slave pode-se instalar as dependências num ambiente virtual ou com `sudo pip3 install -r requirements.txt`

### alterando o IP para execução
* altere para seu IP local nos seguintes lugares, tomando como base a pasta raiz do projeto (colocar localhost não irá funcionar devido ao docker):
	* `master/master/master/settings.py`, linha 28, ALLOWED_HOSTS
	* `repository/repository/repository/settings.py`, linha 28, ALLOWED_HOSTS
	* `slave/slaves.py`, linha 7, REPOSITORY_BASE_URL
	* `master/master/api/management/commands/run_interface.py`, linha 7, REPOSITORY_BASE_URL

### executando a aplicação
* Inicie o servidor executando o seguinte comando dentro da pasta repository `sudo docker-compose up`
* Inicie os escravos executando o comando `python3 slaves.py` de dentro da pasta slave
* Inicie o master executando o comando `sudo docker-compose run migrations python manage.py run_interface`
