from django import forms
from .models import Venda


class VendasExternasForms(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
                    'cliente', 
                    'servico', 
                    'telefone', 
                    'email', 
                    'cidade',
                    'vendedor', 
                    'valor',
                    'consumo',
                    'mes',
                    'ano',
                    'foto_documento',
                    'foto_endereco',
                    'foto_contracheque',
                    'proposta',
                    'contrato',
                ]
        

class Alterar_status_vendas(forms.ModelForm):
    class Meta:
        model = Venda
        fields = [
                'status_venda',
                'status_pg_vendedor',
                ]