from django.urls import path
from . import views


urlpatterns = [
    path('vendascadastrar', views.CadastrarVenda, name='Cadastrar_vendas'),
    
]