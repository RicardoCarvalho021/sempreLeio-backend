##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from django.urls import path
from .views import Usuario_SignUp

urlpatterns = [
    path('usuario/',Usuario_SignUp.as_view()), 
]