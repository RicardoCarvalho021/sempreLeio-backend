##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from django.urls import path
from .views import Postagem_New, Postagem_Ultimas, Postagem_Visivel, Postagem_Relevante, Postagem_Interessante, Postagem_Destaque, Postagem_Avalia

urlpatterns = [
    path('postagem/',Postagem_New.as_view()), 
    path('postagem/ultimas',Postagem_Ultimas.as_view()), 
    path('postagem/<int:postagem_id>/visivel',Postagem_Visivel.as_view()),
    path('postagem/<int:postagem_id>/interessante',Postagem_Interessante.as_view()),
    path('postagem/<int:postagem_id>/relevante',Postagem_Relevante.as_view()),
    path('postagem/<int:postagem_id>/destaque',Postagem_Destaque.as_view()),
    path('postagem/<int:postagem_id>/avalia/<int:conceito>',Postagem_Avalia.as_view()),
]