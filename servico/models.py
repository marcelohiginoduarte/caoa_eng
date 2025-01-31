from django.db import models
from .validators import validar_telefone
from lista_vendedores.models import ListaVendedores

class Servico(models.Model):

    tipo_servicos = [
        ('Eng_Solar', 'Energia solar'),
        ('LT', 'Loteamento'),
        ('PDE', 'PDE'),
        ('HD', 'Hidraulica'),
    ]

    status_servico = [
        ('V' ,'Visita'),
        ('I' ,'Iniciado'),
        ('Co' ,'Contrato'),
        ('A' ,'Andamento'),
        ('E' ,'Execucao'),
        ('C' ,'Concluido'),
        ('P' ,'Pendente'),
    ]

    Mes = [
    ('Janeiro', 'Jan'),
    ('Fevereiro', 'Feb'),
    ('Marco', 'Mar'),
    ('Abril', 'Apr'),
    ('maio', 'May'),
    ('Junho', 'Jun'),
    ('Julho', 'Jul'),
    ('Agosto', 'Aug'),
    ('Setembro', 'Sep'),
    ('Outubro', 'Oct'),
    ('Novembro', 'Nov'),
    ('Dezembro', 'Dec'),
    ]

    cliente = models.CharField(max_length=150, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    tipo_serviço = models.CharField(choices=tipo_servicos,max_length=14, default='Eng_Solar')
    status = models.CharField(choices=status_servico, max_length=10, default='V')
    cidade = models.CharField(max_length=150, blank=True, null=True)
    valor_empreendimento = models.DecimalField(max_digits=10, decimal_places=2) 
    valor_custos = models.DecimalField(max_digits=10, decimal_places=2)
    valor_lucro = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(blank=False, null=False)
    mes = models.CharField(max_length=10, choices=Mes)
    ano = models.CharField(max_length=4, blank=True)
    foto_documento = models.FileField(upload_to='documentos/')
    comoprovante_endereco = models.FileField(upload_to='documentos/')
    comoprovante_renda = models.FileField(upload_to='documentos/')
    vendedor = models.ForeignKey(ListaVendedores, on_delete=models.CASCADE)


    def clean(self):
        validar_telefone(self.telefone)

    def __str__(self):
        return self.cliente