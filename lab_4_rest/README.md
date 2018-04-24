## Instalação
### pré requisitos
* docker
* docker-compose
* python3

### instalação das outras dependências do projeto
* Na pasta master e repository execute o comando:
```
# docker-compose build
```

* Na pasta slave pode-se instalar as dependências num ambiente virtual ou com o comando:
```
sudo pip3 install -r requirements.txt
```

## Execução
### alterando o IP para execução
* altere para seu IP local nos seguintes lugares, tomando como base a pasta raiz do projeto (colocar localhost não irá funcionar devido ao docker):
	* `master/master/master/settings.py`, linha 28, ALLOWED_HOSTS
	* `repository/repository/repository/settings.py`, linha 28, ALLOWED_HOSTS
	* `slave/slaves.py`, linha 7, REPOSITORY_BASE_URL
	* `master/master/api/management/commands/run_interface.py`, linha 7, REPOSITORY_BASE_URL

### executando a aplicação
* Inicie o servidor executando o seguinte comando dentro da pasta repository
```
# docker-compose up
```

* Inicie os escravos executando o comando de dentro da pasta slave:
```
$ python3 slaves.py
```

* Inicie o master executando o comando:
```
# docker-compose run migrations python manage.py run_interface`
```
