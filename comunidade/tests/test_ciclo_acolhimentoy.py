from urllib import response
import requests
import json
import jsonpath
from django.test import TestCase
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from comunidade.views import MinhasComunidades, Comunidade_Seek, SolicitarAcolhimento, AcolherSolicitacao

class TesteAcolhimentoTestCase(TestCase):

    appUrl = "http://127.0.0.1:8000"
   
    @classmethod
    def setUpTestData(cls):
        pass

    def teste_ciclo_Acolhimento(self):
        # testes de integração
        factory = APIRequestFactory()
        view = SolicitarAcolhimento.as_view()
        usuario = User.objects.get(username='vicente')

        # CDU-20
        request = factory.get(self.appUrl + '/membro/0/solicitar/')
        force_authenticate(request, user=usuario)
        resposta = view(request, 0)

## Comunidade informada inexistente.
        self.assertEqual(resposta.status_code,404)

        request = factory.get(self.appUrl + '/membro/1/solicitar/')
        force_authenticate(request, user=usuario)
        resposta = view(request, 1)

## Usuário autenticado é admistrador da comunidade informada.
        self.assertEqual(resposta.status_code,400)

        usuario = User.objects.get(username='andre')
        request = factory.get(self.appUrl + '/membro/1/solicitar/')
        force_authenticate(request, user=usuario)
        resposta = view(request, 1)

## Já existe uma solicitação do usuário para a comunidade.
        self.assertEqual(resposta.status_code,404)

        usuario = User.objects.get(username='vicente')
        request = factory.get(self.appUrl + '/membro/2/solicitar/')
        force_authenticate(request, user=usuario)
        resposta = view(request, 2)

## Foi solicitado seu acolhimento junto ao administrador da comunidade.
        self.assertEqual(resposta.status_code,201)

        # CDU-27
        view = AcolherSolicitacao.as_view()

        usuario = User.objects.get(username='ricardo')
        request = factory.get(self.appUrl + '/membro/0/acolher/')
        force_authenticate(request, user=usuario)
        resposta = view(request, 0)

## Solicitação de acolhimento informada inexistente.
        self.assertEqual(resposta.status_code,404)

        request = factory.get(self.appUrl + '/membro/3/acolher/')
        force_authenticate(request, user=usuario)
        resposta = view(request, 3)

## Usuário autenticado NÃO é admistrador da comunidade informada.
        self.assertEqual(resposta.status_code,400)

        usuario = User.objects.get(username='andre')
        request = factory.get(self.appUrl + '/membro/3/acolher/')
        force_authenticate(request, user=usuario)
        resposta = view(request, 3)

## O membro foi acolhido na comunidade.
        self.assertEqual(resposta.status_code,200)