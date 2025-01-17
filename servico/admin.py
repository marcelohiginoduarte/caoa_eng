from django.contrib import admin
from .models import Servico


class Servicos(admin.ModelAdmin):
    list_display = ('cliente', 'tipo_serviço', 'valor_empreendimento')
    list_display_links = ('cliente', 'tipo_serviço', 'valor_empreendimento')

admin.site.register(Servico, Servicos)


