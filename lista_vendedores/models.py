from django.db import models
from decimal import Decimal

class ListaVendedores(models.Model):
    nome = models.CharField(max_length=200, unique=True, blank=False, null=False)
    Telefone = models.CharField(max_length=15,unique=True, blank=False, null=False)
    pix = models.CharField(max_length=15, blank=False, null=False)
    comissao_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False, default=Decimal('0.00'))


    def __str__(self):
        return self.nome
