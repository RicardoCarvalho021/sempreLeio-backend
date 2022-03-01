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

from django.contrib.auth.models import User
from main.models import Usuario

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['pk','username','password','first_name','last_name','email']
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
       }

class UsuarioSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Usuario
        fields = '__all__'
