from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/vendedor', views.criar_vendedor, name='cadastrarvendedor'),
    
]