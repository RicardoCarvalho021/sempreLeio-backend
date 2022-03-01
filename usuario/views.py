from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import UserSerializer
from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status
from main.models import Usuario, Cidade

from datetime import datetime
from django.db import transaction

# Create your views here.
class Usuario_SignUp(APIView):
    #permission_classes = [IsAuthenticated]
    #authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):

#   Cria um novo usuario.

        serializer = UserSerializer(data=request.data) 
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()
                    newuser = User.objects.get(pk=serializer.data['pk'])
                    newuser.set_password(serializer.data['password'])
                    newuser.save()
                    name = newuser.first_name + ' ' + newuser.last_name
                    agora = datetime.now().date()
                    cidade_id = 1
                    usuario = Usuario()
                    usuario.nome=name
                    usuario.cpf='99999999999'
                    usuario.email=newuser.email
                    usuario.data_admissao=agora
                    usuario.eh_ativo=True
                    usuario.user=newuser
                    usuario.residencia_id=cidade_id
                    usuario.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
               Response(serializer.data, status=status.HTTP_400_BAD_REQUEST) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)