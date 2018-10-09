# api
Api em django com template com tela de login, cadastro e adm.

# Como rodar?
Criar banco:

> **Comando:** $ mysql -u usuario -p senha

> **Comando:** $ CREATE DATABASE med;

> **Comando:** $ CREATE USER 'med_user'@'localhost' IDENTIFIED BY '123';

> **Comando:** $ GRANT ALL PRIVILEGES ON * . * TO 'med_user'@'localhost';

Crie uma virtualenv, Python3:

> **Comando:** $ virtualenv env-api

 Entre na virtualenv:
 
> **Comando:** $ source env-api/bin/activate

Entre na pasta do repositorio:

> **Comando:** $ cd api/

Instalei o Modulo:

> **Comando:** $ pip install . -U

Comandos para iniciar a API:

> **Comando:** $ python3 manage.py migrate

> **Comando:** $ python3 manage.py runserver






