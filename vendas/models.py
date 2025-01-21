from django.db import models
from servico.validators import validar_telefone
from decimal import Decimal
from .utils import calcular_comissao, formatar_valor_comissao

class Venda(models.Model):

    tipo_servico = [
        ('SL', 'Solar'),
        ('LT', 'Loteamento'),
        ('PDE', 'PDE'),
        ('HD', 'Hidraulico'),
    ]

    status_vendas = [
        ('env_banc', 'Enviado ao banco'),
        ('aprov_banc', 'Banco aprovado'),
        ('repr_banc', 'Banco reprovado'),
        ('cancel_banc', 'Banco cancelado'),
        ('cancel_client', 'Cliente cancelado'),
    ] 

    pagamento_vendedor = [
        ('agr_vd', 'Aguardando venda'),
        ('agr_banc', 'Aguardando o banco'),
        ('real', 'Realizado'),
        ('pend', 'Pendente'),
        ('Cancelado', 'Cancelado'),
        
    ]

    Mes = [
        ('Jan', 'Jan'),
        ('Fev', 'Fev'),
        ('Mar', 'Mar'),
        ('Abr', 'Abr'),
        ('Mai', 'Mai'),
        ('Jun', 'Jun'),
        ('Jul', 'Jul'),
        ('Ago', 'Ago'),
        ('Set', 'Set'),
        ('Out', 'Out'),
        ('Nov', 'Nov'),
        ('Dez', 'Dez'),
    ]


    cliente = models.CharField(max_length=150, blank=False, null=False)
    servico = models.CharField(choices=tipo_servico, max_length=15, blank=False, null=False)
    telefone = models.CharField(max_length=15, blank=False, null=False)
    consumo = models.CharField(max_length=30, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comissao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    mes = models.CharField(max_length=4, choices=Mes)
    ano = models.CharField(max_length=4, blank=True)
    vendendor = models.CharField(max_length=150, blank=True)
    status_venda = models.CharField(choices=status_vendas, max_length=15, blank=False, null=False, default='env_banc')
    status_pg_vendedor = models.CharField(choices=pagamento_vendedor, max_length=15, blank=False, null=False, default='agr_vd')
    foto_documento = models.FileField(upload_to='documentos/')
    foto_endereco = models.FileField(upload_to='documentos/')
    foto_contracheque = models.FileField(upload_to='documentos/')

    
    def save(self, *args, **kwargs):
        if self.valor:
            self.comissao = calcular_comissao(self.valor)
        super().save(*args, **kwargs)

    def clean(self):
        validar_telefone(self.telefone)

    def formatar_valor(self):
        return formatar_valor_comissao(self.valor)

    def formatar_comissao(self):
        return formatar_valor_comissao(self.comissao)
    

    def clean_valor(self):
        if self.valor:
            self.valor = Decimal(self.valor.replace('.', '').replace(',', '.'))

    def __str__(self):
        return self.cliente