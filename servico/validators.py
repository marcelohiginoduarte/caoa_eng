from django.core.exceptions import ValidationError
import re

def validar_telefone(valor):
    padrao = r'^\+?1?\d{9,15}$'
    if not re.match(padrao, valor):
        raise ValidationError("O número de telefone deve estar no formato: '+999999999'. Até 15 dígitos são permitidos.")
