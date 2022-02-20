##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from datetime import datetime
from logging import exception

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Comunidade, Topico, UsuarioComunidade
from comunidade.serializers import MinhasComunidadesSerializer, UltimasComunidadesSerializer, ComunidadeSerializer, UsuarioComunidadeSerializer
from topico.serializers import TopicoSerializer

#-----------------------------
class Comunidade_Crud(APIView):
#----------------------------- 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 

    def post(self, request, format=None):

    #   CDU-10   
    #   Usuário autenticado cria uma nova comunidade.
 
        serializer = ComunidadeSerializer(data=request.data)
        if serializer.is_valid():
            usuario = request.user.usuario
            serializer.save(data_publicacao = datetime.now().date(), proprietario = usuario)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, comunidade_id):

    #   CDU-01
    #   O proprietario altera os dados de sua comunidade.

        try:
            comunidade = Comunidade.objects.get (pk=comunidade_id)
        except:
            return Response(data={'Erro':'Comunidade informada não existe.'},status=status.HTTP_404_NOT_FOUND)            
            
        if (request.user.usuario != comunidade.proprietario):
            return Response(data={'Erro':'Usuário autenticado NÃO é admistrador da comunidade informada.'},status=status.HTTP_400_BAD_REQUEST)

        data_original = comunidade.data_publicacao
        serializer = ComunidadeSerializer(comunidade, data=request.data)
        if serializer.is_valid():
            serializer.save(data_publicacao=data_original)
            return Response(data={'Sucesso':'Os dados da comunidade foram alterados.'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

#--------------------------------
class MinhasComunidades(APIView):
#--------------------------------
# CDU-13
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):

    #   Lista as 20 últimas comunidades de propriedade do usuário autenticado
    #   em ordem decrescente de data.

        comunidades = Comunidade.objects.filter(proprietario=request.user.usuario).order_by('-data_publicacao') [:20]
        if comunidades:
            serializer = MinhasComunidadesSerializer(comunidades, many=True)
            return Response(serializer.data)        
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

#-----------------------------
class Comunidade_Get(APIView):
#-----------------------------
# CDU-31
# Para usuarios não autenticados

    def get(self, request, comunidade_id):

    #   Retorna os dados de comunidade informada.

        try:
            comunidade = Comunidade.objects.get(pk=comunidade_id)
        except:
            Response(data={'Erro':'Comunidade informada não existe.'},status=status.HTTP_404_NOT_FOUND)

        serializer = ComunidadeSerializer(comunidade)
        return Response(serializer.data,status=status.HTTP_200_OK)        

#------------------------------
class Comunidade_Seek(APIView):
#------------------------------
# CUD-21
# Para usuarios não autenticados

    def get(self, request, filtro):

    #   Retorna lista de comunidades para o filtro informado.

        comunidades = Comunidade.objects.filter(Q(denominacao__icontains=filtro) | Q(descricao__icontains=filtro)).filter(eh_visivel=True, eh_publica=True) [:20]
        if comunidades:
            serializer = UltimasComunidadesSerializer(comunidades, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)        
        return Response(data={'Erro':'Nenhuma comunidade foi encontrada para o filtro informado.'},status=status.HTTP_404_NOT_FOUND)        

#--------------------------------
class Comunidade_Topicos(APIView):
#--------------------------------
# CDU-16
# Para usuarios não autenticados

    def get(self, request, comunidade_id):

    #   Retorna lista de topicos para a comunidade informada.
        topicos = Topico.objects.filter(comunidade_id=comunidade_id).order_by('-data_publicacao') [:20]
        if topicos:
            serializer = TopicoSerializer(topicos, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)        
        return Response(data={'Erro':'Não existem tópicos para a comunidade informada.'},status=status.HTTP_404_NOT_FOUND)

#--------------------------------------
class ComunidadesQueParticipo(APIView):
#--------------------------------------
# CDU-28
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):

    #   Lista as últimas 20 comunidades que o usuário autenticado
    #   eh membro em ordem decrescente de data.

        membro_de = UsuarioComunidade.objects.filter(usuario=request.user.usuario, situacao=1)
        comunidades = [entry.comunidade_id for entry in membro_de]
        comunidades = Comunidade.objects.filter(pk__in=comunidades).order_by('-data_publicacao') [:20]
        if comunidades.count() > 0:
            serializer = UltimasComunidadesSerializer(comunidades, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)        
        return Response(data={'Erro':'Usuário não participa de qualquer comunidade.'},status=status.HTTP_404_NOT_FOUND)

#------------------------------
class Comunidade_List(APIView):
#------------------------------
# CDU-30
# Para usuarios não autenticados

    def get(self, request, format=None):

    #   Lista as últimas 20 comunidades visíveis e públicas, em ordem decrescente de data.

        comunidades = Comunidade.objects.filter(eh_visivel=True, eh_publica=True).order_by('-data_publicacao') [:20]
        if comunidades:
            serializer = UltimasComunidadesSerializer(comunidades, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)        
        return Response(data={'Erro':'Não existem comunidades.'},status=status.HTTP_404_NOT_FOUND)

#--------------------------------------
class Comunidade_Membros(APIView):
#--------------------------------------
# CDU-12
# Para usuarios não autenticados

    def get(self, request, comunidade_id):

    #   Lista todos os membros de uma comunidade

        try:
            comunidade = Comunidade.objects.get(pk=comunidade_id)
        except:
            return Response(data={'Erro':'Comunidade informada não existe.'},status=status.HTTP_404_NOT_FOUND)

        membros = comunidade.membros()
        if membros.count() == 0:
            return Response(data={'Erro':'Comunidade informada não possui membros.'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = UsuarioComunidadeSerializer(membros, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK) 

#-------------------------------------
class SolicitarAcolhimento(APIView):
#-------------------------------------
# CDU-20
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, comunidade_id):

    #   Usuário autenticado solicita acolhimento à comunidade informada.

        try:
            comunidade = Comunidade.objects.get(pk=comunidade_id)
        except:
            return Response(data={'Erro':'Solicitação informada inexistente.'},status=status.HTTP_404_NOT_FOUND)    

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

#---------------------------------
class AcolherSolicitacao(APIView):
#---------------------------------
# CDU-27
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, usuariocomunidade_id):

    #   Proprietário da comunidade acolhe a solicitacao informada.

        try:
            uc = UsuarioComunidade.objects.get(pk=usuariocomunidade_id)
        except:
            return Response(data={'Erro':'Solicitação de acolhimento informada inexistente.'},status=status.HTTP_404_NOT_FOUND)    

        if (uc.situacao > 0):
            return Response(data={'Erro':'Não é possível acolher a solicitação informada.'},status=status.HTTP_400_BAD_REQUEST)

        if (request.user.usuario != uc.comunidade.proprietario):
            return Response(data={'Erro':'Usuário autenticado NÃO é admistrador da comunidade informada.'},status=status.HTTP_400_BAD_REQUEST)

        uc.situacao = 1
        uc.data_situacao = timezone.now()
        uc.save()
        return Response(data={'Sucesso':'O membro foi acolhido na comunidade.'},status=status.HTTP_200_OK)

#---------------------------------
class RevogarSolicitacao(APIView):
#---------------------------------
# CDU-07
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, usuariocomunidade_id):

    #   Proprietário da comunidade exclui a solicitacao informada.

        try:
            uc = UsuarioComunidade.objects.get(pk=usuariocomunidade_id)
        except:
            return Response(data={'Erro':'Solicitação de acolhimento informada inexistente.'},status=status.HTTP_404_NOT_FOUND)    

        if (request.user.usuario != uc.comunidade.proprietario):
            return Response(data={'Erro':'Usuário autenticado NÃO é admistrador da comunidade informada.'},status=status.HTTP_400_BAD_REQUEST)

        uc.delete()
        return Response(data={'Sucesso':'A solicitação de acolhimento do usuário foi revogada.'},status=status.HTTP_200_OK)

#---------------------------------
class RecusarSolicitacao(APIView):
#---------------------------------
# CDU-24
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, usuariocomunidade_id):

    #   Proprietário da comunidade exclui a solicitacao de acolhimento informada,
    #   desde que esta encontre-se em situação SOLICITADO.

        try:
            uc = UsuarioComunidade.objects.get(pk=usuariocomunidade_id)
        except:
            return Response(data={'Erro':'Solicitação de acolhimento informada inexistente.'},status=status.HTTP_404_NOT_FOUND)    

        if uc.situacao == 1:
            return Response(data={'Erro':'Membro já foi acholhido. O administrador poderá bani-lo da comunidade.'},status=status.HTTP_404_NOT_FOUND)

        if (request.user.usuario != uc.comunidade.proprietario):
            return Response(data={'Erro':'Usuário autenticado NÃO é admistrador da comunidade informada.'},status=status.HTTP_400_BAD_REQUEST)

        uc.situacao = -1
        uc.save()
        return Response(data={'Sucesso':'A solicitação de acolhimento do usuário foi negada.'},status=status.HTTP_200_OK)

