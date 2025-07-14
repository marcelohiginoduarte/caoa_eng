from django import forms
from servico.models import Servico

class CadastrarServicoforms(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'cliente',
            'telefone',
            'tipo_servico',
            'status',
            'cidade',
            'valor_empreendimento',
            'valor_custos',
            'valor_lucro',
            'email',
            'mes',
            'ano',
            'foto_documento',
            'comoprovante_endereco',
            'comoprovante_renda',
        ]