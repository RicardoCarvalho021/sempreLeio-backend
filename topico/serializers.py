##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from rest_framework import serializers
from main.models import Topico
from postagem.serializers import PostagemSerializer

class TopicoSerializer(serializers.ModelSerializer):
    postagens = serializers.SerializerMethodField()
    #postagens = PostagemSerializer(many=True, read_only=True)
    class Meta:
        model = Topico
        #fields = '__all__'
        fields = ['id','titulo','comunidade', 'postagens']


    def get_postagens(self, topico):
        return PostagemSerializer(topico.postagem_set.all(), many=True).data        
