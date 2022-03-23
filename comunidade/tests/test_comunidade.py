from urllib import response
import requests
import json
import jsonpath
from django.test import TestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from comunidade.views import MinhasComunidades, Comunidade_Seek

class TesteComunidadeTestCase(TestCase):

    appUrl = "http://127.0.0.1:8000"
    
    @classmethod
    def setUpTestData(cls):
        pass

    def teste_PesquisarComunidade(self):
        # CDU-21

        factory = APIRequestFactory()
        usuario = User.objects.get(username='vicente')
        view = Comunidade_Seek.as_view()

        request = factory.get(self.appUrl + '/comunidade/filtro/pesquisar/')
        filtro = 'Machado'
        force_authenticate(request, user=usuario)
        resposta = view(request,filtro)        
        self.assertEqual(resposta.status_code,200)

    def teste_MinhasComunidades(self):
        # CDU-13
        factory = APIRequestFactory()
        view = MinhasComunidades.as_view()
        usuario = User.objects.get(username='vicente')

        request = factory.get(self.appUrl + '/comunidade/minhas/')
        force_authenticate(request, user=usuario)
        resposta = view(request)

        self.assertEqual(resposta.status_code,200)
##
        usuario = User.objects.get(username='ricardo')

        request = factory.get(self.appUrl + '/comunidade/minhas/')
        force_authenticate(request, user=usuario)
        resposta = view(request)

        self.assertEqual(resposta.status_code,200)
##
        usuario = User.objects.get(username='andre')

        request = factory.get(self.appUrl + '/comunidade/minhas/')
        force_authenticate(request, user=usuario)
        resposta = view(request)

        self.assertEqual(resposta.status_code,200)

