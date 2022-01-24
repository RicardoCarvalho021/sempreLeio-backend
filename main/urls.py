##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (distribuido)
# SempreLeio 2021.2 
# Vicente Limeira
# Lista de recursos
##----------------------------------------------------------

from django.urls import path, include
from .views import Comunidade_List_New, ComunidadesQueParticipo, MinhasComunidades, SolicitarAcolhimento, AcolherSolicitacao
from .views import Comunidade_Crud

urlpatterns = [
    path('comunidade/<int:comunidade_id>',Comunidade_Crud.as_view()), 
    path('comunidade/',Comunidade_List_New.as_view()), 
    path('comunidade/minhas',MinhasComunidades.as_view()),
    path('membro/<int:comunidade_id>/solicitar/',SolicitarAcolhimento.as_view()),
    path('membro/<int:usuariocomunidade_id>/acolher/',AcolherSolicitacao.as_view()),
    path('comunidade/queparticipo',ComunidadesQueParticipo.as_view()),

]