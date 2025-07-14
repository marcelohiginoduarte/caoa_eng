from django import forms
from .models import Venda


class VendasExternasForms(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
            'cliente', 'servico', 'telefone', 'email', 'cidade', 'vendedor',
            'valor', 'consumo', 'mes', 'ano',
            'foto_documento', 'foto_endereco', 'foto_contracheque', 'proposta', 'contrato',
        ]

    grupo_cliente = ['cliente', 'servico', 'telefone', 'email', 'cidade', 'vendedor']
    grupo_venda = ['valor', 'consumo', 'mes', 'ano']
    grupo_documentos = ['foto_documento', 'foto_endereco', 'foto_contracheque', 'proposta', 'contrato']
        

class Alterar_status_vendas(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
                'status_venda',
                'status_pg_vendedor',
                ]