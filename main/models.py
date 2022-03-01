##----------------------------------------------------------
# IFRN-TADS
# Projeto de desenvolvimento de software (distribuido)
# SempreLeio 2021.1
# Vicente Limeira
# Classes de Domínio:
#   Cidade, Usuario, Comunidade, Topico, Postagem, 
#   UsuarioComunidade, UsuarioPostagem.
##----------------------------------------------------------

from datetime import datetime, timedelta
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.db.models import Avg

### Relacionamentos (1/n):

class Cidade(models.Model):

    MA = 'MA'
    PI = 'PI'
    CE = 'CE'
    RN = 'RN'
    PB = 'PB'
    PE = 'PE'
    AL = 'AL'
    SE = 'SE'
    BA = 'BA'

    ES = 'ES'
    MG = 'MG'
    RJ = 'RJ'
    SP = 'SP'

    PR = 'PR'
    SC = 'SC'
    RS = 'RS'

    MT = 'MT'
    MS = 'MS'
    GO = 'GO'
    TO = 'TO'
    DF = 'DF'
    
    RR = 'RR'
    RO = 'RO'
    AC = 'AC'
    AM = 'AM'
    PA = 'PA'
    AP = 'AP'      

    UNIDADES_DA_FEDERACAO = [
        (MA, 'Maranhão'),
        (PI, 'Piauí'),
        (CE, 'Ceará'),
        (RN, 'Rio Grande do Norte'),
        (PB, 'Paraíba'),
        (PE, 'Pernambuco'),
        (AL, 'Alagoas'),
        (SE, 'Sergipe'),
        (BA, 'Bahia'),

        (ES, 'Espírito Santo'),
        (MG, 'Minas Gerais'),
        (RJ, 'Rio de Janeiro'),
        (SP, 'São Paulo'),

        (PR, 'Paraná'),
        (SC, 'Santa Catarina'),
        (RS, 'Rio Grande do Sul'),

        (MT, 'Mato Grosso'),
        (MS, 'Mato Grosso do Sul'),
        (GO, 'Goiás'),
        (TO, 'Tocantins'),
        (DF, 'Distrito Federal'),
        
        (RR, 'Roraima'),
        (RO, 'Rondônia'),
        (AC, 'Acre'),
        (AM, 'Amazonas'),
        (PA, 'Pará'),
        (AP, 'Amapá'),       
    ]

    denominacao = models.CharField(max_length = 100)
    uf = models.CharField(
        max_length=2,
        choices=UNIDADES_DA_FEDERACAO,
    )

    def __str__(self):
        return self.denominacao

class Usuario(models.Model):
    nome = models.CharField(max_length = 100)
    cpf = models.CharField(max_length = 11)
    email = models.EmailField(max_length = 100)
    data_admissao  = models.DateTimeField('Data de admissão', default=timezone.now)
    eh_ativo = models.BooleanField()
    residencia = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    comunidades = models.ManyToManyField('Comunidade', through='UsuarioComunidade')
    postagens = models.ManyToManyField('Postagem', through='UsuarioPostagem')
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete = models.SET_NULL,
        null = True
    )

    def __str__(self):
        return self.nome

class Comunidade(models.Model):
    denominacao = models.CharField(max_length = 100)
    descricao = models.TextField()
    eh_publica = models.BooleanField()
    eh_visivel = models.BooleanField()
    #imagem     = models.ImageField(upload_to='media/posts', blank=False, verbose_name='IMAGEM DA POSTAGEM')
    data_publicacao  = models.DateField()
    proprietario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    def __str__(self):
        return self.denominacao

    def pedidos_pendentes(self):
        return self.usuariocomunidade_set.filter(situacao=0).order_by('-data_situacao')

    def membros(self):
        return self.usuariocomunidade_set.filter(situacao=1).order_by('data_situacao')

    def eh_nova(self):
        return self.data_publicacao+timedelta(days=30) >= timezone.now().date()

    def eh_proprietario(self, usuario):
        return usuario == self.proprietario

    def eh_membro(self, user):
        existe = self.usuariocomunidade_set.filter(situacao=1).filter(usuario=user).exists()
        return existe

class Topico(models.Model):
    titulo = models.CharField(max_length = 100)
    data_publicacao  = models.DateField()
    comunidade = models.ForeignKey(Comunidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    def postagens(self):
        return Postagem.objects.filter(topico=self).order_by('-data_publicacao') [:20]


class Postagem(models.Model):
    texto = models.TextField(null=True, blank=True, verbose_name="Texto da postagem")
    eh_visivel = models.BooleanField(default=False,null=False,blank=False)
    data_publicacao  = models.DateField(null=True, blank=True)
    arquivo_de_midia = models.CharField(max_length=200, null=True, blank=True, verbose_name="Arquivo de mídia anexado")
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE, verbose_name="Tópico?")
    signatario = models.ForeignKey(Usuario, on_delete=models.CASCADE,verbose_name="Signatário?")

    def conceito(self):
        up = UsuarioPostagem.objects.filter(postagem=self).aggregate(Avg('conceito'))
        result = up['conceito__avg']
        if not result:
            return 0
        return result

    def avaliacoes(self):
        avaliacoes = UsuarioPostagem.objects.filter(postagem=self).count()
        return avaliacoes

    def __str__(self):
        return self.texto

### Relacionamentos (n/n)

class UsuarioComunidade(models.Model):

    SOLICITADO = 0
    ACEITO = 1
    RECUSADO = -1

    SITUACAO = [
        (SOLICITADO, 'Solicitado'),        
        (ACEITO, 'Aceito'),        
        (RECUSADO, 'Recusado'),        
    ]

    situacao = models.SmallIntegerField(choices=SITUACAO)
    data_situacao  = models.DateTimeField(null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    comunidade = models.ForeignKey(Comunidade, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.nome + '(' + str(self.situacao) + ')' + self.comunidade.denominacao

class UsuarioPostagem(models.Model):

    INTERESSANTE = 2
    RELEVANTE = 4
    DESTAQUE = 8

    CONCEITOS = [
        (INTERESSANTE, 'Interessante'),
        (RELEVANTE, 'Relevante'),
        (DESTAQUE, 'Destaque'),
    ]

    data_avaliacao  = models.DateTimeField('Data de avaliacao',default=timezone.now)
    conceito  = models.SmallIntegerField(choices=CONCEITOS)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)

    def __str__(self):
        return 'UsuarioPostagem'
