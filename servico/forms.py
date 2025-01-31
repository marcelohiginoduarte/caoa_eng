from django import forms
from .models import Servico

class CadastrarServicoforms(forms.ModelForm):
    class Meta:
        model = Servico
        fields = [
            'cliente',
            'telefone',
            'tipo_serviço',
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