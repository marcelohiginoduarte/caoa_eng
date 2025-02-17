from django.contrib import admin
from .models import Servico


class Servicos(admin.ModelAdmin):
    list_display = ('cliente', 'id', 'tipo_serviço', 'valor_empreendimento','vendedor')
    list_display_links = ('cliente', 'tipo_serviço', 'valor_empreendimento')

admin.site.register(Servico, Servicos)


