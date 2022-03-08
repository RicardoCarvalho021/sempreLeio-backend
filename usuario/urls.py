##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (corporativo)
# SempreLeio 2021.2
# Vicente Limeira
##----------------------------------------------------------

from django.urls import path
from .views import Usuario_SignUp, UserDetailsView

urlpatterns = [
    path('usuario/',Usuario_SignUp.as_view()), 
### Iury (8-3-2022)
    path('userdetails/', UserDetailsView.as_view()),
]