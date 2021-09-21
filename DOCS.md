# ControleNF

# Documentação
```
Afim de documentar o backend, foi preparado esse MD, para a descrição do uso da API
e como rodar a aplicação em ambiente local.
```

# Heroku
```
O link para acessar o backend no heroku é
https://controlenf.herokuapp.com/
```

# POSTMAN
```
O link para acessar a documentação do postman é
https://documenter.getpostman.com/view/2899621/UUxtGWqV
```

# Executar servidor local

### Tecnologias empregadas
- Django v3.2.7 LTS
- Python 3.9 (VirtualEnv)

### Como rodar o projeto

##### 1. Criar uma virtualenv para instalação das dependências
```
virtualenv --python=$(which python3.9) env-controle
```

##### 2. Execução da virtualenv
```
source env-controle/bin/activate
```

##### 3. Instalação das dependências (Pasta raiz do projeto, e venv ativada (Passo 2))
```
pip install -r requirements.txt
```

##### 4. Criar .env

```
ENVIRONMENT=development
DEBUG=True
SECRET_KEY="43aq7j+1w=ucbzht59s14q@qk9dwfg-1!@23d@m^dk&5v8rn0w"

DATABASE_NAME=controlenf
DATABASE_PASSWORD=123
DATABASE_USER=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
```


##### 5. Executar migrações

```
./manage.py makemigrations
./manage.py runserver
```


##### 6. Executar servidor

```
./manage.py runserver

Pronto estará rodando na porta 8000
```