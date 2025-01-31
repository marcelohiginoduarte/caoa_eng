from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import CriarVendedorForms
from .models import ListaVendedores
from vendas.models import Venda


def ver_todos_vendedores(request):
    ver_vendedores = ListaVendedores.objects.all()

    total_vendas_por_vendedor = {}
    total_comissao = {}

    for vendedor in ver_vendedores:
        total_vendas = (Venda.objects.filter(vendedor=vendedor.id, status_venda='aprov_banc').aggregate(total=Sum('valor'))['total'])
        toal_vendas_comissao = (Venda.objects.filter(vendedor=vendedor.id, status_pg_vendedor='real').aggregate(total=Sum('comissao'))['total'])
        total_vendas = total_vendas if total_vendas else 0
        toal_vendas_comissao = toal_vendas_comissao if toal_vendas_comissao else 0
        total_vendas_por_vendedor[vendedor.nome] = total_vendas
        total_comissao[vendedor.nome] = toal_vendas_comissao

    return render(request, 'listavendedorestodos.html', {'ver_vendedores': ver_vendedores, 'total_vendas_por_vendedor':total_vendas_por_vendedor, 'total_comissao':total_comissao})

def criar_vendedor(request):
    
    if request.method == 'POST':
        form = CriarVendedorForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vertodosvendedores')
        
    else:
        form = CriarVendedorForms()
    
    return render(request, 'vendedores_cadastrar.html', {'form': form})