from decimal import Decimal
import locale
from lista_vendedores.models import ListaVendedores


def calcular_comissao(valor):
    try:
        valor_comissao = vendedor.comissao_venda
        valor_decimal = Decimal(valor_comissao) if valor_comissao else Decimal('0.00')
        return valor_decimal * Decimal('0.05')  # Calcula a comissão com base no valor
    except (ValueError, TypeError):
        return Decimal('0.00')


def formatar_valor_comissao(valor):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(valor, grouping=True) if valor else 'R$ 0,00'
