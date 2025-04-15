from django import template

register = template.Library()

@register.simple_tag
def soma_valores(dicionario, vendedores):
    total = sum(dicionario.get(vendedor.nome, 0) for vendedor in vendedores)
    return total

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 0) 