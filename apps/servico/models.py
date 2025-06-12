from django.db import models
from .validators import validar_telefone
from lista_vendedores.models import ListaVendedores
from django.db.models import Sum

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

    MESES = [
        ('Janeiro', 'Jan'),
        ('Fevereiro', 'Fev'),
        ('Março', 'Mar'),
        ('Abril', 'Abr'),
        ('Maio', 'Mai'),
        ('Junho', 'Jun'),
        ('Julho', 'Jul'),
        ('Agosto', 'Ago'),
        ('Setembro', 'Set'),
        ('Outubro', 'Out'),
        ('Novembro', 'Nov'),
        ('Dezembro', 'Dez'),
    ]

    cliente = models.CharField("Nome do cliente", max_length=150, null=False, blank=False)
    telefone = models.CharField(max_length=15, null=False, blank=False)
    tipo_serviço = models.CharField(choices=tipo_servicos, max_length=14, default='Eng_Solar')
    status = models.CharField(choices=status_servico, max_length=10, default='V')
    cidade = models.CharField(max_length=150, blank=True, null=True)
    valor_empreendimento = models.DecimalField(max_digits=10, decimal_places=2)
    valor_custos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor_lucro = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    email = models.EmailField()
    mes = models.CharField(max_length=10, choices=MESES)
    ano = models.CharField(max_length=4, blank=True)
    foto_documento = models.FileField(upload_to='documentos/')
    comoprovante_endereco = models.FileField(upload_to='documentos/')
    comoprovante_renda = models.FileField(upload_to='documentos/')
    vendedor = models.ForeignKey(ListaVendedores, on_delete=models.CASCADE)
    projeto_ativo = models.BooleanField(default=True)

    def clean(self):
        validar_telefone(self.telefone)

    def calcular_custos_e_lucro(self):
        total_custos = self.acompanhamentodespesasprojeto_set.aggregate(soma=Sum('valor'))['soma'] or 0
        self.valor_custos = total_custos
        self.valor_lucro = self.valor_empreendimento - total_custos

    def save(self, *args, **kwargs):
        self.calcular_custos_e_lucro()
        if self.status == 'C':
            self.projeto_ativo = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cliente