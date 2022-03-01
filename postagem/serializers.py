##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from rest_framework import serializers
from main.models import Postagem, Topico, Usuario, Comunidade

class ComunidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunidade
        fields = ['pk','denominacao']

class UsuarioSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Usuario
        fields = ['pk','nome']

class PostagemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Postagem
        fields = ['pk','texto','signatario','conceito','avaliacoes']

class TopicoSerializer(serializers.ModelSerializer):
    comunidade = ComunidadeSerializer(read_only=True)
    class Meta:
        model = Topico
        fields = ['pk','titulo','comunidade']

class UltimasPostagensSerializer(serializers.ModelSerializer):
    signatario = UsuarioSerializer(read_only=True)
    topico = TopicoSerializer(read_only=True)

    class Meta:
        model = Postagem
        fields = ['pk','conceito','avaliacoes','eh_visivel','texto','data_publicacao','signatario','topico']

