from django.contrib import admin
from servico.models import Servico


class Servicos(admin.ModelAdmin):
    list_display = ('cliente', 'id', 'tipo_servico', 'valor_empreendimento','vendedor')
    list_display_links = ('cliente', 'tipo_servico', 'valor_empreendimento')

admin.site.register(Servico, Servicos)


