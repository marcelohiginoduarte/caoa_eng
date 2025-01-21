from decimal import Decimal
import locale

#Comissão de venda dos vendedores
def calcular_comissao(valor):
    if valor:
        return Decimal(valor) * Decimal('0.05')
    return Decimal('0.00')


#Formater para o modelo moeda brasileira
def formatar_valor_comissao(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(valor, grouping=True) if valor else 'R$ 0,00'
