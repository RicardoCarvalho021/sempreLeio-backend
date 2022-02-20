##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from django.urls import path
from .views import Topico_Crud, Topico_Postagens

urlpatterns = [
    path('topico/<int:topico_id>/postagens',Topico_Postagens.as_view()), 
    path('topico/',Topico_Crud.as_view()),
    path('topico/<int:topico_id>',Topico_Crud.as_view()), 
]