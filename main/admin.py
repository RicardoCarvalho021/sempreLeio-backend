from django.contrib import admin
from .models import Comunidade, Topico, Postagem, Usuario, Cidade, UsuarioComunidade

class UsuarioComunidadeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'situacao', 'data_situacao', 'usuario','comunidade')  

class ComunidadeAdmin(admin.ModelAdmin):
    list_display = ('denominacao', 'data_publicacao', 'eh_publica', 'eh_visivel','pk')  

class TopicoAdmin(admin.ModelAdmin):
    pass

class PostagemAdmin(admin.ModelAdmin):
    pass

class UsuarioAdmin(admin.ModelAdmin):
    pass

class CidadeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comunidade, ComunidadeAdmin)
admin.site.register(Topico, TopicoAdmin)
admin.site.register(Postagem, PostagemAdmin)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Cidade, CidadeAdmin)
admin.site.register(UsuarioComunidade, UsuarioComunidadeAdmin)