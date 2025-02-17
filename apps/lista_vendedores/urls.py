from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/vendedor', views.criar_vendedor, name='cadastrarvendedor'),
    path('verlistavendedor', views.ver_todos_vendedores, name='vertodosvendedores'),
    
]