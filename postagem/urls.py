##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from django.urls import path
from .views import Postagem_New

urlpatterns = [
    path('postagem',Postagem_New.as_view()), 
]