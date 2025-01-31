from django.db import models
from servico.validators import validar_telefone
from decimal import Decimal
from .utils import calcular_comissao, formatar_valor_comissao
from servico.models import Servico
from lista_vendedores.models import ListaVendedores

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
    cidade = models.CharField(max_length=150, blank=True, null=True)
    consumo = models.CharField(max_length=30, blank=True, null=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    comissao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    mes = models.CharField(max_length=4, choices=Mes)
    ano = models.CharField(max_length=4, blank=True)
    vendedor = models.ForeignKey(ListaVendedores, on_delete=models.CASCADE, related_name='venda')
    status_venda = models.CharField(choices=status_vendas, max_length=15, blank=False, null=False, default='env_banc')
    status_pg_vendedor = models.CharField(choices=pagamento_vendedor, max_length=15, blank=False, null=False, default='agr_vd')
    foto_documento = models.FileField(upload_to='documentos/')
    foto_endereco = models.FileField(upload_to='documentos/')
    foto_contracheque = models.FileField(upload_to='documentos/')
    proposta = models.FileField(upload_to='documentos/', blank=True, null=True)
    contrato = models.FileField(upload_to='documentos/',blank=True, null=True)

    
    def save(self, *args, **kwargs):
        if self.pk:
            venda_antiga = Venda.objects.get(pk=self.pk)
            if venda_antiga.status_venda != self.status_venda and self.status_venda == 'aprov_banc':
                Servico.objects.create(
                    cliente=self.cliente,
                    telefone=self.telefone,
                    tipo_serviço=self.servico,
                    status='V',
                    valor_empreendimento=self.valor,
                    valor_custos=Decimal(self.valor) * Decimal('0.7'),  
                    valor_lucro=Decimal(self.valor) * Decimal('0.3'),                   
                    email=self.email,
                    mes=self.mes,
                    ano=self.ano,
                    foto_documento=self.foto_documento,
                    comoprovante_endereco=self.foto_endereco,
                    comoprovante_renda=self.foto_contracheque,
                )

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