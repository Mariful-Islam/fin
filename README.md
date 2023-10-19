# Digital Banking System FIN

## Introduction

This is a very simple banking system where perform transder money from one person to another person. It is made with django, django rest framework and react.

## Requirement

1. python
2. django
3. django rest framework
4. django corsheaders
5. simple jwt

## Steps

1. First of all, install python from official website https://python.org.
2. Create virtual environment by this command --- "python -m venv [Environment Name]".
3. Activate the virtual environment by this command --- "./[Environment Name]/Scripts/activate.
4. Install django by this command --- "pip install django" to develop backend logic.
5. Install django rest framework by this command --- "pip install djangorestframework" to build rest api.
6. Install corsheaders by this command --- "pip install django-corsheaders" for sharing api to different domain.
7. Install simple-jwt by this command --- "pip install djangorestframework-simplejwt"
8. Install git from their official website.
9. To download the project file by this command --- "git clone https://github.com/Mariful-Islam/fin"
10. Goto project directory using "cd/fin" and open with code editor.
11. Type the two command to create database migration --- "python manage.py makemigrations" then "python manage.py migrate.
12. To create superuser using this command --- "python manage.py createsuperuser" and enter name, email and password.
13. To execute the web application --- "python manage.py runserver"

## Description

1. A user can send money to another user and also receive money. So, the amount of money that was sent is minus from the sender account and added to the receiver account.
2. Easily send and receive money through REST API which is developed using Django Rest Framework. 
3. A react app was also developed to test the REST API such transfer money using the API.
4. The application (FIN) records the ledger and transaction. Also, generates transaction ID to identify the transaction.
5. Download ledger and transactions record as csv file.
6. The application shows the list of users which have bank accounts.
7. Every user has to create a bank account otherwise he/she cannot send or receive money. Every bank account has a unique account ID which is suggested or customized in the bank account creation time. 
8. In the react FIN app, a user can perform all actions.
9. Apply algorithms, data structure and my knowledge regularly to increase efficiency, scalability, reusability, security. 

