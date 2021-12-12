##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from .models import Comunidade, Topico, Postagem, Usuario, UsuarioComunidade
from .serializers import MinhasComunidadesSerializer, UltimasComunidadesSerializer, ComunidadeSerializer, UsuarioComunidadeSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404

from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

##------------------------------------------------------
#                                             Comunidade
##------------------------------------------------------

##from rest_framework import viewsets
##class UltimasComunidadesViewSet(viewsets.ModelViewSet):
##    queryset = Comunidade.objects.filter(eh_visivel=True, eh_publica=True).order_by('-data_publicacao') [:20]
##    serializer_class = ComunidadeSerializer
   
class Comunidade_List_New(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, format=None):

#   Lista as últimas 20 comunidades visíveis e públicas,
#   em ordem decrescente de data.

        comunidades = Comunidade.objects.filter(eh_visivel=True, eh_publica=True).order_by('-data_publicacao') [:20]
        if comunidades:
            serializer = UltimasComunidadesSerializer(comunidades, many=True)
            return Response(serializer.data)        
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request, format=None):

#   Cria uma nova comunidade.

        serializer = ComunidadeSerializer(data=request.data)
        if serializer.is_valid():
            usuario = request.user.usuario
            serializer.save(data_publicacao = datetime.now().date(), proprietario = usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MinhasComunidades(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):

#       Lista todas as comunidades do usuário autenticado
#       em ordem decrescente de data.

        comunidades = Comunidade.objects.filter(proprietario=request.user.usuario)
        if comunidades:
            serializer = MinhasComunidadesSerializer(comunidades, many=True)
            return Response(serializer.data)        
        return Response(status=status.HTTP_404_NOT_FOUND)

class SolicitarAcolhimento(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, comunidade_id):

#       Solicita acolhimento a comunidade informada.

        comunidade = Comunidade.objects.get(pk=comunidade_id)
        if (request.user.usuario == comunidade.proprietario):
            return Response(data={'Erro':'Usuário autenticado é admistrador da comunidade informada.'},status=status.HTTP_400_BAD_REQUEST)
        else:
            uc = UsuarioComunidade.objects.filter(comunidade_id = comunidade_id,usuario_id = request.user.usuario.id)
            if (not uc):
                uc = UsuarioComunidade()
                uc.situacao = 0
                uc.data_situacao = timezone.now()
                uc.comunidade = comunidade
                uc.usuario = request.user.usuario
                uc.save()
                return Response(data={'Sucesso':'Foi solicitado seu acolhimento junto ao administrador da comunidade.'},status=status.HTTP_201_CREATED)
            else:            
                return Response(data={'Erro':'Já existe uma solicitação do usuário para a comunidade'},status=status.HTTP_404_NOT_FOUND)

class AcolherSolicitacao(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, usuariocomunidade_id):

#       Acolhe uma solicitacao informada.

        uc = UsuarioComunidade.objects.get(pk=usuariocomunidade_id)
        if not uc:
            return Response(data={'Erro':'Solicitação de acolhimento não existe.'},status=status.HTTP_404_NOT_FOUND)

        if (uc.situacao > 0):
            return Response(data={'Erro':'Não é possível acolher a solicitação informada.'},status=status.HTTP_400_BAD_REQUEST)

        comunidade = Comunidade.objects.get(pk=uc.comunidade.id)
        if (request.user.usuario != comunidade.proprietario):
            return Response(data={'Erro':'Usuário autenticado NÃO é admistrador da comunidade informada.'},status=status.HTTP_400_BAD_REQUEST)

        uc.situacao = 1
        uc.data_situacao = timezone.now()
        uc.save()
        return Response(data={'Sucesso':'O membro foi acolhido na comunidade.'},status=status.HTTP_200_OK)

class ComunidadesQueParticipo(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):

#       Lista todas as comunidades que o usuário autenticado
#       eh membro em ordem decrescente de data.

        membro_de = UsuarioComunidade.objects.filter(usuario=request.user.usuario)
        comunidades = [entry.comunidade_id for entry in membro_de]
        comunidades = Comunidade.objects.filter(pk__in=comunidades).order_by('-data_publicacao')
        if comunidades:
            serializer = UltimasComunidadesSerializer(comunidades, many=True)
            return Response(serializer.data)        
        return Response(status=status.HTTP_404_NOT_FOUND)

"""
SolicitarAcolhimento:  comunidade/membro/<int:comunidade_id>/solicitar/          
AcolherSolicitacao:    comunidade/membro/<int:pk>/acolher/
RecusarSolicitacao:    comunidade/membro/recusar/pk
CancelarSolicitacao:   comunidade/membro/cancelar/pk
"""