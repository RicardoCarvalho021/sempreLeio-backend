from urllib import response
import requests
import json
import jsonpath
from django.test import TestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from comunidade.views import MinhasComunidades, Comunidade_Seek, SolicitarAcolhimento, AcolherSolicitacao

class TesteLoginTestCase(TestCase):

    appUrl = "http://127.0.0.1:8000"
    login_vicente = {"username": "vicente","password": "teste@123"}
    
    @classmethod
    def setUpTestData(cls):
        pass

    def teste_Login(self):
        #arquivo = open('login.json','r')
        #dados = json.loads(arquivo.read())
        resposta = requests.post(self.appUrl + '/api/v1/rest-auth/login/',json=self.login_vicente)
        dados = json.loads(resposta.text)
        key = dados['key']
        self.assertEqual(resposta.status_code,200)
        chave = "Token " + key
        header = {"accept": "application/json", "Authentication" : chave}