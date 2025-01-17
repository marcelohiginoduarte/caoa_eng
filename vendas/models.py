from django.db import models
from servico.validators import validar_telefone

class Venda(models.Model):

    tipo_servico = [
        ('SL', 'Solar'),
        ('LT', 'Loteamento'),
        ('PDE', 'PDE'),
        ('HD', 'Hidraulico'),
    ]


    cliente = models.CharField(max_length=150, blank=False, null=False)
    servico = models.CharField(choices=tipo_servico, max_length=15, blank=False, null=False)
    telefone = models.CharField(max_length=15, blank=False, null=False)
    consumo = models.CharField(max_length=30, blank=True, null=True)
    valor = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    vendendor = models.CharField(max_length=150, blank=True)
    foto_documento = models.FileField(upload_to='documentos/')
    foto_endereco = models.FileField(upload_to='documentos/')
    foto_contracheque = models.FileField(upload_to='documentos/')


    def clean(self):
        validar_telefone(self.telefone)

    def __str__(self):
        return self.cliente