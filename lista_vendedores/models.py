from django.db import models

class ListaVendedores(models.Model):
    nome = models.CharField(max_length=200, unique=True, blank=False, null=False)
    Telefone = models.CharField(max_length=15,unique=True, blank=False, null=False)
    pix = models.CharField(max_length=15, blank=False, null=False)
    comissao_venda = models.CharField(max_length=15, blank=False, null=False)


    def __str__(self):
        return self.nome
