from django.contrib import admin
from .models import ListaVendedores


class ListaVendedorAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    list_display_links = ('nome',)

admin.site.register(ListaVendedores, ListaVendedorAdmin)
