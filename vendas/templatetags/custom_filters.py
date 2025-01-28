from django import template

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

