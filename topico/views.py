##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------
from datetime import datetime

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Comunidade, Postagem, Topico
from topico.serializers import TopicoSerializer
from postagem.serializers import PostagemSerializer

#--------------------------------
class Topico_Postagens(APIView):
#--------------------------------
# CDU-15
# Para usuarios não autenticados

    def get(self, request, topico_id):

    #   Retorna lista de postagens para o tópico informado.

        postagens = Postagem.objects.filter(topico_id=topico_id).order_by('-data_publicacao') [:20]
        if postagens:
            serializer = PostagemSerializer(postagens, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)        
        return Response(data={'Erro':'Não existem postagens para o tópico informado.'},status=status.HTTP_404_NOT_FOUND)

#-----------------------------
class Topico_Crud(APIView):
#----------------------------- 
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]    

    def post(self, request, format=None):
    #   CDU-18
    #   Usuário proprietario de uma comunidade cria novo topico.

        serializer = TopicoSerializer(data=request.data)     
        if serializer.is_valid():
            try:
                comunidade = Comunidade.objects.get(pk=serializer.validated_data['comunidade'].id)
            except:
                return Response(data={'Erro':'Comunidade inexistente.'},status=status.HTTP_400_BAD_REQUEST)                

            if (request.user.usuario != comunidade.proprietario):
                return Response(data={'Erro':'Usuário autenticado NÃO é admistrador da comunidade informada.'},status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save(data_publicacao = datetime.now().date())
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, topico_id):
    #   CDU-29
    #   O proprietario de uma comunidade altera os dados de um topico.

        try:
            topico = Topico.objects.get(pk=topico_id)
        except:
            return Response(data={'Erro':'Tópico informado não existe.'},status=status.HTTP_404_NOT_FOUND)            

        if (request.user.usuario != topico.comunidade.proprietario):
            return Response(data={'Erro':'Usuário autenticado NÃO é admistrador desta comunidade.'},status=status.HTTP_400_BAD_REQUEST)

        data_original = topico.data_publicacao
        serializer = TopicoSerializer(topico,data=request.data)      
        if serializer.is_valid():
            serializer.save(data_publicacao=data_original)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'Erro':'Dados enviados são inválidos ou incompletos.'},status=status.HTTP_400_BAD_REQUEST)
