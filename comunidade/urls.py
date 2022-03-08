##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from django.urls import path, include
from .views import Comunidade_Crud, MinhasComunidades, Comunidade_Get, Comunidade_Seek, Comunidade_Topicos, ComunidadesQueParticipo, Comunidade_List, Comunidade_Membros, SolicitarAcolhimento, AcolherSolicitacao, RevogarSolicitacao, RecusarSolicitacao

urlpatterns = [
    path('comunidade/',Comunidade_Crud.as_view()), 
    path('comunidade/<int:comunidade_id>/',Comunidade_Crud.as_view()),
    path('comunidade/minhas/',MinhasComunidades.as_view()),

    path('comunidade/<int:comunidade_id>/detalhar/',Comunidade_Get.as_view()), 
    path('comunidade/<str:filtro>/pesquisar/',Comunidade_Seek.as_view()), 
    path('comunidade/pesquisar/',Comunidade_List.as_view()), 

    path('comunidade/<int:comunidade_id>/topicos/',Comunidade_Topicos.as_view()), 
    path('comunidade/queparticipo/',ComunidadesQueParticipo.as_view()),
    path('comunidade/ultimas/',Comunidade_List.as_view()), 
    path('comunidade/<int:comunidade_id>/membros/',Comunidade_Membros.as_view()), 

    path('membro/<int:comunidade_id>/solicitar/',SolicitarAcolhimento.as_view()),
    path('membro/<int:usuariocomunidade_id>/acolher/',AcolherSolicitacao.as_view()),
    path('membro/<int:usuariocomunidade_id>/banir/',RevogarSolicitacao.as_view()),
    path('membro/<int:usuariocomunidade_id>/recusar/',RecusarSolicitacao.as_view()),
    
]