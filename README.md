[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

# BPMN

This project implements part of a semantic framework directed to Business Process Management Notation.

## Configuração

### Usando Docker

Requires Docker and docker-compose installed. 
1. [Download docker here](https://www.docker.com/products/docker-desktop) 
2. [Download and Install docker-compose here](https://docs.docker.com/compose/install/)

In root directory run ```docker-compose up```. App will start and run in port localhost:3000

#### Debug

Run bash inside the application container. Run ```docker exec -it sfdjango_djangoapp_1 /bin/bash``` in another terminal while the container is running.

### Sem Docker

Passo 1: Instalação do Python 3.7
    Windows: Certifique-se que se trata da versão de 64 bits e escolha no instalador a opção de inclusão 
    da variável de ambiente no path. Após instalado, verifique a instalação através do comando 
    python --version no terminal do windows que você utiliza.

Passo 2: Instalação do virtualenv
    No terminal, faça a intalação do virualenv através do comando "pip install virtualenv".

Passo 3: Instalar o ambiente virtual na pasta do projeto.
    Comando: virtualenv venv
    Observação: Caso esteja trabalhando no Windows sem uma IDE como PyCharm, é necessário ativar e desativar o ambiente virtual.
    O arquivo activate ativa o ambiente e o deactivate o desativa. Ambos scripts se encontram na pasta Script do venv criado.
    Ainda do Windows, a execução de scripts pode estar desabilitada. Logo, para executar o comando activate será necessário 
    definir a política de execução para o usuário através do comando "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser".

Passo 4: Instalar os pacotes necessários.
    Para instalar os pacotes necessários, com o ambiente virtual ativo, execute o comando  "pip install -r requirements.txt".
    Obs.: No Windows será necessário ter instalado o Microsoft C++ Build Tools para que os pacotes possam ser compilados.

Passo 5: Instalar o PostgreeSQL.
    Observação: O projeto foi desenvolvido com a versão 13 do PostgreeSQL. Versões superiores do Python podem apresentar incompatibilidade
    no Windows.

Passo 6 (opcional): Criar o DB da aplicação caso não exista.
    No Windows o banco de dados pode ser criado através da aplicação PGAdmin. O nome do banco de dados deve ser
    bpmn e a senha 123456. Alterações nessas informações implicam em configuração do arquivo settings.py.

Passo 7: Criar super usuário para a aplicação.
    Comando: python manage.py createsuperuser

Passo 8: Criar as tabelas da aplicação no banco de dados.
    Comando: python manage.py makemigrations
             python manage.py migrate

Passo 9: Teste a intalação do django rodando o servidor local.
    Comando: python manage.py runserver

python -c "import nltk; nltk.download('punkt')"


### Seed Database

python3 manage.py shell < seed.py