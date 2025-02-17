from django import template
from decimal import Decimal
import locale
from lista_vendedores.models import ListaVendedores
from vendas.models import Venda

register = template.Library()

@register.filter
def get_venda(dictionary, key):

    return dictionary.get(key, 0)


@register.filter
def formatar_valor(valor):
    if valor is None:
        return 'R$ 0,00'
    valor_formatado = f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
    
    return f"R$ {valor_formatado}"

@register.filter
def calcular_comissao(valor, vendedor_id):
    try:
        vendedor = ListaVendedores.objects.get(id=vendedor_id)
        venda = Venda.objects.filter(vendedor=vendedor).first()

        if venda:
            valor_venda = venda.valor
            valor_comissao = vendedor.comissao_venda
            valor_decimal = Decimal(valor_venda) * Decimal(valor_comissao) / Decimal('100')
            return f"R$ {valor_decimal:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")
        return "R$ 0,00"

    except (ListaVendedores.DoesNotExist, Venda.DoesNotExist, ValueError, TypeError) as e:
        return "R$ 0,00"

@register.filter
def formatar_valor_comissao(valor):
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency(valor, grouping=True) if valor else 'R$ 0,00'
    except locale.Error:
        return f'R$ {valor:.2f}'