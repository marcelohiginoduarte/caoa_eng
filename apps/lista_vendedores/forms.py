from django import forms
from .models import ListaVendedores

class CriarVendedorForms(forms.ModelForm):
    class Meta:
        model = ListaVendedores
        fields = ['nome', 'Telefone', 'pix', 'comissao_venda']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'Telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'pix': forms.TextInput(attrs={'class': 'form-control'}),
            'comissao_venda': forms.NumberInput(attrs={'class': 'form-control'}),
        }