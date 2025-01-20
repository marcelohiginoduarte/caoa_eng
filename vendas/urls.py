from django.urls import path
from . import views


urlpatterns = [
    path('vendascadastrar', views.CadastrarVenda, name='Cadastrar_vendas'),
    path('vendasporvendedor', views.vendas_vendedor_logado, name='vendasporvendedor'),
    path('vendasstatus/<int:venda_id>', views.status_vendas, name='alterar_status_venda'),
    path('venda/<int:venda_id>/detalhes/', views.detalhe_vendas, name='detalhes_venda'),
]