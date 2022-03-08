##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from datetime import datetime

#from django.db.models import Q
#from django.core.exceptions import ObjectDoesNotExist
#from django.utils import timezone
#from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import status 
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Topico, Postagem, UsuarioPostagem
from .serializers import PostagemSerializer, UltimasPostagensSerializer

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
        autenticado = request.user.usuario
        if serializer.is_valid():
            try:
                topico = serializer.validated_data['topico']
                topico = Topico.objects.get(pk=topico.pk)
            except:
                return Response(data={'Erro':'Tópico informado não existe.'},status=status.HTTP_404_NOT_FOUND)

            if request.user.is_superuser or topico.comunidade.eh_membro(autenticado) or topico.comunidade.eh_proprietario(autenticado):
                serializer.save(data_publicacao = datetime.now().date(), signatario=autenticado)
            else:
                return Response(data={'Erro':'Usuário autenticado NÃO possui permissão para contribuir com a comunidade.'},status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------
class Postagem_Ultimas(APIView):
#----------------------------- 
# CDU-25   
# Para usuarios não autenticados

    def get(self, request, format=None):

    #   Lista 20 ultimas postagens visiveis

        postagens = Postagem.objects.filter(eh_visivel=True).order_by('-data_publicacao') [:20]
        if postagens.count() > 0:
            serializer = UltimasPostagensSerializer(postagens, many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)        
        return Response(data={'Erro':'Nenhuma postagem foi registrada até o momento.'},status=status.HTTP_404_NOT_FOUND)        

#-----------------------------
class Postagem_Visivel(APIView):
#----------------------------- 
# CDU-02   
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 

    def get(self, request, postagem_id):

    #   Altera opção de visibilidade da postagem (toggle)
        autenticado = request.user.usuario

        try:
            postagem = Postagem.objects.get(pk=postagem_id)
        except:
            return Response(data={'Erro':'Postagem inexistente.'},status=status.HTTP_404_NOT_FOUND)                   

        if request.user.is_superuser or postagem.topico.comunidade.eh_proprietario(autenticado) or postagem.signatario == autenticado:
            postagem.eh_visivel = not postagem.eh_visivel
            postagem.save()
        else:
            return Response(data={'Erro':'Usuário autenticado NÃO possui permissão para alterar a postagem.'},status=status.HTTP_400_BAD_REQUEST)            
        return Response(data={'Sucesso':'A visibilidade da postagem foi alterada.'},status=status.HTTP_200_OK)        

#-----------------------------
class Postagem_Relevante(APIView):
#----------------------------- 
# CDU-05
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 

    def get(self, request, postagem_id):

    #   Insere/Altera avaliacao relevante da postagem
        autenticado = request.user.usuario

        try:
            postagem = Postagem.objects.get(pk=postagem_id)
        except:
            return Response(data={'Erro':'Postagem inexistente.'},status=status.HTTP_404_NOT_FOUND)                   

        if postagem.signatario == autenticado:
            return Response(data={'Erro':'Usuário signatário NÃO pode avaliar sua postagem.'},status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser or postagem.topico.comunidade.eh_proprietario(autenticado) or postagem.topico.comunidade.eh_membro(autenticado):
            up = UsuarioPostagem.objects.filter(usuario=autenticado, postagem_id=postagem_id)
            if (not up):
                up = UsuarioPostagem()
                up.data_avaliacao = timezone.now()
                up.conceito = 4
                up.usuario = autenticado
                up.postagem = postagem
                up.save()
            else:
                for avaliacao in up:
                    avaliacao.conceito = 4
                    avaliacao.save()
        else:
            return Response(data={'Erro':'Usuário autenticado NÃO possui permissão para alterar a postagem.'},status=status.HTTP_400_BAD_REQUEST)            
        return Response(data={'Sucesso':'A postagem foi avaliada como RELEVANTE.'},status=status.HTTP_200_OK)        

#-----------------------------
class Postagem_Destaque(APIView):
#----------------------------- 
# CDU-05
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 

    def get(self, request, postagem_id):

    #   Insere/Altera avaliacao destaque da postagem
        autenticado = request.user.usuario

        try:
            postagem = Postagem.objects.get(pk=postagem_id)
        except:
            return Response(data={'Erro':'Postagem inexistente.'},status=status.HTTP_404_NOT_FOUND)                   

        if postagem.signatario == autenticado:
            return Response(data={'Erro':'Usuário signatário NÃO pode avaliar sua postagem.'},status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser or postagem.topico.comunidade.eh_proprietario(autenticado) or postagem.topico.comunidade.eh_membro(autenticado):
            up = UsuarioPostagem.objects.filter(usuario=autenticado, postagem_id=postagem_id)
            if (not up):
                up = UsuarioPostagem()
                up.data_avaliacao = timezone.now()
                up.conceito = 8
                up.usuario = autenticado
                up.postagem = postagem
                up.save()
            else:
                for avaliacao in up:
                    avaliacao.conceito = 8
                    avaliacao.save()
        else:
            return Response(data={'Erro':'Usuário autenticado NÃO possui permissão para alterar a postagem.'},status=status.HTTP_400_BAD_REQUEST)            
        return Response(data={'Sucesso':'A postagem foi avaliada como DESTAQUE.'},status=status.HTTP_200_OK)        

#-----------------------------
class Postagem_Interessante(APIView):
#----------------------------- 
# CDU-05
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 

    def get(self, request, postagem_id):

    #   Insere/Altera avaliacao destaque da postagem
        autenticado = request.user.usuario

        try:
            postagem = Postagem.objects.get(pk=postagem_id)
        except:
            return Response(data={'Erro':'Postagem inexistente.'},status=status.HTTP_404_NOT_FOUND)                   

        if postagem.signatario == autenticado:
            return Response(data={'Erro':'Usuário signatário NÃO pode avaliar sua postagem.'},status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser or postagem.topico.comunidade.eh_proprietario(autenticado) or postagem.topico.comunidade.eh_membro(autenticado):
            up = UsuarioPostagem.objects.filter(usuario=autenticado, postagem_id=postagem_id)
            if (not up):
                up = UsuarioPostagem()
                up.data_avaliacao = timezone.now()
                up.conceito = 2
                up.usuario = autenticado
                up.postagem = postagem
                up.save()
            else:
                for avaliacao in up:
                    avaliacao.conceito = 2
                    avaliacao.save()
        else:
            return Response(data={'Erro':'Usuário autenticado NÃO possui permissão para alterar a postagem.'},status=status.HTTP_400_BAD_REQUEST)            
        return Response(data={'Sucesso':'A postagem foi avaliada como INTERESSANTE.'},status=status.HTTP_200_OK)        

#-----------------------------
class Postagem_Avalia(APIView):
#----------------------------- 
# CDU-05
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication] 

    def get(self, request, postagem_id, conceito):

    #   Insere/Altera avaliacao da postagem
        autenticado = request.user.usuario

        try:
            postagem = Postagem.objects.get(pk=postagem_id)
        except:
            return Response(data={'Erro':'Postagem inexistente.'},status=status.HTTP_404_NOT_FOUND)                   

        if postagem.signatario == autenticado:
            return Response(data={'Erro':'Usuário signatário NÃO pode avaliar sua postagem.'},status=status.HTTP_400_BAD_REQUEST)

        if request.user.is_superuser or postagem.topico.comunidade.eh_proprietario(autenticado) or postagem.topico.comunidade.eh_membro(autenticado):
            if conceito not in [2,4,8]:
                return Response(data={'Erro':'O conceito deve ser informado corretamente: [2=INTERESSANTE], [4=RELEVANTE], [8=DESTAQUE]'},status=status.HTTP_400_BAD_REQUEST)

            up = UsuarioPostagem.objects.filter(usuario=autenticado, postagem_id=postagem_id)
            if (not up):
                up = UsuarioPostagem()
                up.data_avaliacao = timezone.now()
                up.conceito = conceito
                up.usuario = autenticado
                up.postagem = postagem
                up.save()
            else:
                for avaliacao in up:
                    avaliacao.conceito = conceito
                    avaliacao.save()
        else:
            return Response(data={'Erro':'Usuário autenticado NÃO possui permissão para alterar a postagem.'},status=status.HTTP_400_BAD_REQUEST)            
        return Response(data={'Sucesso':'Sua avaliação foir registrada.'},status=status.HTTP_200_OK)        
