##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (distribuido)
# SempreLeio 2021.1
# Vicente Limeira
##----------------------------------------------------------
# Revisado em 23-9-2021

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime
from rest_framework import status 
from rest_framework.response import Response
from .models import Comunidade, Topico, Postagem, Usuario
from .serializers import ComunidadeSerializer, TopicoSerializer, PostagemSerializer
from django.conf.urls import url

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

##--------------------------------------------------------
#                                               Comunidade
##--------------------------------------------------------
serializer_class=ComunidadeSerializer
@api_view(['GET', 'POST'])
#permission_classes([IsAuthenticated])
def ListarOuCriarComunidade(request):
    
    """
    Uma requisição GET lista as comunidades existentes, e por POST cria uma nova comunidade.
    """

    if request.method == 'GET':
        comunidades = Comunidade.objects.all().order_by('-data_publicacao')
        if comunidades:
            serializer = ComunidadeSerializer(comunidades, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)          

    elif request.method == 'POST':
        serializer = ComunidadeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(data_publicacao = datetime.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
#permission_classes([IsAuthenticated])
def ManterComunidade(request, id):
    """
    Informando o ID da comunidade em uma requisição GET o sistema recupera dados daquela comunidade. Em uma requisição PUT o sistema altera dados daquela comunidade e em requisição DELETE exclui a comunidade.
    """
    try:
        comunidade = Comunidade.objects.get(pk=id)
    except Comunidade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ComunidadeSerializer(comunidade)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ComunidadeSerializer(comunidade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comunidade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def ProcurarComunidade(request, pesquisa):
    """
    Informando um texto em uma requisição GET o sistema lista as comunidades que contém aquele texto.
    """        
    comunidades = Comunidade.objects.filter(Q(denominacao__icontains=pesquisa) | Q(descricao__icontains=pesquisa))
    if comunidades:
        serializer = ComunidadeSerializer(comunidades, many=True)
        return Response(serializer.data)        
    return Response(status=status.HTTP_404_NOT_FOUND)

##----------------------------------------------------
#                                               Topico
##----------------------------------------------------

@api_view(['GET', 'POST'])
def ListarOuCriarTopico(request):
    """
    Uma requisição GET lista os tópicos existentes, e uma requisição POST cria um novo topico.
    """    
    if request.method == 'GET':
        topicos = Topico.objects.all().order_by('-data_publicacao')
        if topicos:
            serializer = TopicoSerializer(topicos, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)          

    elif request.method == 'POST':
        serializer = TopicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(data_publicacao = datetime.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def ManterTopico(request, id):
    """
    Informando o ID do tópico em uma requisição GET o sistema recupera dados daquele tópico. Em uma requisição PUT o sistema altera dados daquele tópico e em requisição DELETE exclui o tópico.
    """

    try:
        topico = Topico.objects.get(pk=id)
    except Topico.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TopicoSerializer(topico)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TopicoSerializer(topico, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        topico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def ProcurarTopico(request, pesquisa):
    """
    Informando um texto em uma requisição GET o sistema lista os tópicos que contém aquele texto.
    """        
    topicos = Topico.objects.filter(titulo__icontains=pesquisa)
    if topicos:
        serializer = TopicoSerializer(topicos, many=True)
        return Response(serializer.data)        
    return Response(status=status.HTTP_404_NOT_FOUND)

##------------------------------------------------------
#                                               Postagem
##------------------------------------------------------

@api_view(['GET', 'POST'])
def ListarOuCriarPostagem(request):
    """
    Uma requisição GET lista as postagens existentes, e uma requisição POST cria uma nova postagem.
    """    
    if request.method == 'GET':
        postagens = Postagem.objects.all().order_by('-data_publicacao')
        if postagens:
            serializer = PostagemSerializer(postagens, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)          

    elif request.method == 'POST':
        serializer = PostagemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(data_publicacao = datetime.now())
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['GET', 'PUT', 'DELETE'])
def ManterPostagem(request, id):
    """
    Informando o ID da postagem em uma requisição GET o sistema recupera dados daquela postagem. Em uma requisição PUT o sistema altera dados daquela postagem e em requisição DELETE exclui a postagem.
    """
    try:
        postagem = Postagem.objects.get(pk=id)
    except Postagem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostagemSerializer(postagem)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PostagemSerializer(postagem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        postagem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
@api_view(['GET'])
def ProcurarPostagem(request, pesquisa):
    """
    Informando um texto em uma requisição GET o sistema lista as postagens que contém aquele texto.
    """    
    postagens = Postagem.objects.filter(texto__icontains=pesquisa)
    if postagens:
        serializer = PostagemSerializer(postagens, many=True)
        return Response(serializer.data)        
    return Response(status=status.HTTP_404_NOT_FOUND)

##------------------------------------------------------
#                                  Tópicos da Comunidade
##------------------------------------------------------
@api_view(['GET'])
def TopicosDaComunidade(request, id):
    """
    Informando o ID da comunidade em uma requisição GET o sistema lista os tópicos daquela comunidade.
    """
    try:
        comunidade = Comunidade.objects.get(pk=id)
    except Comunidade.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    topicos = Topico.objects.filter(comunidade=comunidade)
    if topicos:
        serializer = TopicoSerializer(topicos, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

##------------------------------------------------------
#                                    Postagens do Topico
##------------------------------------------------------
@api_view(['GET'])
def PostagensDoTopico(request, id):
    """
    Informando o ID do tópico em uma requisição GET o sistema lista as postagens daquele tópico.
    """
    try:
        topico = Topico.objects.get(pk=id)
    except Topico.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    postagens = Postagem.objects.filter(topico = topico)
    if postagens:
        serializer = PostagemSerializer(postagens, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

##------------------------------------------------------
#                                 Comunidades do Usuario
##------------------------------------------------------
@api_view(['GET'])
def ComunidadesDoUsuario(request, id):
    """
    Informando o ID do usuário em uma requisição GET o sistema lista as comunidades daquele usuário.
    """
    try:
        usuario = Usuario.objects.get(pk=id)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    comunidades = Comunidade.objects.filter(proprietario = usuario)
    if comunidades:
        serializer = ComunidadeSerializer(comunidades, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

##------------------------------------------------------
#                                                Topicos
##------------------------------------------------------
from rest_framework.views import APIView
from django.http import Http404
class TopicoPost(APIView):
    """
    Cria uma nova postagem.
    """
    def post(self, request, format=None):
        serializer = TopicoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##------------------------------------------------------
#                                                Topicos
##------------------------------------------------------
class TopicoDetail(APIView):
    """
    Recupera, atualiza ou exclui um topico.
    """
    def get_object(self, pk):
        try:
            return Topico.objects.get(pk=pk)
        except Topico.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TopicoSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TopicoSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        topico = self.get_object(pk)
        topico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)