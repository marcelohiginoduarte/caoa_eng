from django.contrib import admin
from .models import ListaVendedores, VendaMensal


class ListaVendedorAdmin(admin.ModelAdmin):
    list_display = ('nome','id')
    list_display_links = ('nome',)

admin.site.register(ListaVendedores, ListaVendedorAdmin)

class VendaMensalAdmin(admin.ModelAdmin):
    list_display = ('vendedor', 'mes', 'total_vendas','total_comissao')
    list_display_links = ('vendedor',)

admin.site.register(VendaMensal, VendaMensalAdmin)