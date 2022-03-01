from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="SempreLeio API",
      default_version='v1',
      description="Este trabalho eh parte integrante da entrega do projeto final da disciplina PDS Corporativo, IFRN, Campus Central.\nDesenvolvido por Vicente Limeira.",
      contact=openapi.Contact(email="sempreleio@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('comunidade.urls')), 
    path('',include('topico.urls')), 
    path('',include('postagem.urls')), 
    path('',include('usuario.urls')), 
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
]
