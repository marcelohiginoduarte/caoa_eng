from django.contrib import admin
from .models import Venda

class VendaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'id']
    list_display_links = ['cliente']

admin.site.register(Venda, VendaAdmin)