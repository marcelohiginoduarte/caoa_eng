from django import forms
from .models import AcompanhamentoDespesasProjeto


class CriarAcompanhamentoDespesasForms(forms.ModelForm):
    class Meta:
        model = AcompanhamentoDespesasProjeto
        fields=[
            'projeto',
            'descricao',
            'valor',
            'observacao',
        ]