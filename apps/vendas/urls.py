from django.urls import path
from . import views


urlpatterns = [
    path('vendascadastrar', views.CadastrarVenda, name='Cadastrar_vendas'),
    path('vendasporvendedor', views.vendas_vendedor_logado, name='vendasporvendedor'),
    path('vendasstatus/<int:venda_id>', views.status_vendas, name='alterar_status_venda'),
    path('vendas/<int:id>/detalhes/', views.detalhe_vendas, name='detalhes_venda'),
    path('vendas/atualiza/<int:pk>', views.AtualizarVenda.as_view(), name='atualizarvendas'),
    path('vendas/deletar/<int:pk>', views.DeletarVenda.as_view(), name='deletarvenda'),
]