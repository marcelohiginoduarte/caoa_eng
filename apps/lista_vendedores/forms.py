from django import forms
from .models import ListaVendedores

class CriarVendedorForms(forms.ModelForm):
    class Meta:
        model = ListaVendedores
        fields = [
            'nome',
            'Telefone',
            'pix',
            'comissao_venda',
        ]