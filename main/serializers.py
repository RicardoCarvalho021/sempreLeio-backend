##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (distribuido)
# SempreLeio 2021.1
# Vicente Limeira
# Serializadores:
#   Comunidade
##----------------------------------------------------------

from django.db.models.fields.related import ManyToManyField
from rest_framework import serializers
from .models import Comunidade, Topico, Postagem, Usuario, UsuarioComunidade

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['pk','nome']

class UsuarioComunidadeSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(many=False,read_only=True)
    class Meta:
        model = UsuarioComunidade
        fields = ['pk','situacao', 'data_situacao','usuario']

class ComunidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comunidade
        fields = ['pk','denominacao','descricao','data_publicacao', 'eh_publica','eh_visivel','eh_nova']

class ProprietarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['pk','nome']

class UltimasComunidadesSerializer(serializers.ModelSerializer):
    proprietario = ProprietarioSerializer(read_only=True)
    membros = UsuarioComunidadeSerializer(many=True, read_only=True)
    class Meta:
        model = Comunidade
        fields = ['pk','denominacao','descricao','data_publicacao','eh_nova','membros','proprietario']

class MinhasComunidadesSerializer(serializers.ModelSerializer):
    membros = UsuarioComunidadeSerializer(many=True, read_only=True)
    pedidos_pendentes = UsuarioComunidadeSerializer(many=True, read_only=True)
    class Meta:
        model = Comunidade
        fields = ['pk','denominacao','descricao','data_publicacao','eh_nova','membros','pedidos_pendentes']

class TopicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topico
        fields = ['id','titulo','comunidade']

class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postagem
        fields = ['id','texto','topico','signatario']
