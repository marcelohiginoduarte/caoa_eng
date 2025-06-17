from django import forms
from servico.models import Servico
from apps.acompanhamentosfinanceiroprojeto.models import AcompanhamentoDespesasProjeto


class CriarAcompanhamentoDespesasForms(forms.ModelForm):
    class Meta:
        model = AcompanhamentoDespesasProjeto
        fields=[
            'projeto',
            'descricao',
            'valor',
            'observacao',
        ]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['projeto'].queryset = Servico.objects.filter(projeto_ativo=True)