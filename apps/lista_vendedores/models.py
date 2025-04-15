from django.db import models
from decimal import Decimal
from django.utils.timezone import now
from django.contrib.auth.models import User

class ListaVendedores(models.Model):
    nome = models.CharField(max_length=200, unique=True, blank=False, null=False)
    Telefone = models.CharField(max_length=15,unique=True, blank=False, null=False)
    pix = models.CharField(max_length=15, blank=False, null=False)
    comissao_venda = models.IntegerField(blank=False, null=False, default=0)

    def __str__(self):
        return self.nome


class VendaMensal(models.Model):
    vendedor = models.ForeignKey('ListaVendedores', on_delete=models.CASCADE)
    mes = models.CharField(max_length=15)
    ano = models.IntegerField()
    total_vendas = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_comissao = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('vendedor', 'mes', 'ano')

    def __str__(self):
        return f"{self.vendedor.nome} - {self.mes}/{self.ano}"