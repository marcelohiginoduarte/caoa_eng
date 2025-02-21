from django.db import models
from servico.models import Servico

class AcompanhamentoDespesasProjeto(models.Model):
    projeto = models.ForeignKey(Servico, on_delete=models.CASCADE, blank=False, null=False)
    descricao = models.CharField(max_length=150, blank=False, null=False)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)
    data_compra = models.DateField(auto_now_add=True)
    observacao = models.CharField(max_length=350, blank=True, null=True)


    def __str__(self):
        return self.projeto