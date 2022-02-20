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
from django.shortcuts import get_object_or_404

from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Topico
from postagem.serializers import PostagemSerializer

# CDU-02 Esconder/Mostrar publicação (toggle)
# CDU-05 Avaliar publicação (interessante, relevante ou destaque)
# CDU-17 Exibir últimas publicações

#-----------------------------
class Postagem_New(APIView):
#----------------------------- 
# CDU-25   
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]    

    def post(self, request, format=None):

    #   Usuário membro ou proprietario de uma comunidade submete nova postagem.

        serializer = PostagemSerializer(data=request.data)
        
        if serializer.is_valid():

            try:
                topico = Topico.objects.get(pk=serializer.data['topico'])
            except:
                return Response(data={'Erro':'Tópico informado não existe.'},status=status.HTTP_404_NOT_FOUND)

            if not request.user.usuario.is_superuser:
                if not topico.comunidade.eh_proprietario(request.user.usuario):
                    if not topico.comunidade.eh_membro(request.user.usuario):
                        return Response(data={'Erro':'Usuário autenticado NÃO possui permissão para contribuir com a comunidade.'},status=status.HTTP_400_BAD_REQUEST)

            serializer.save(data_publicacao = datetime.now().date())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
