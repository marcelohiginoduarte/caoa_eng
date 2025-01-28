from django.shortcuts import render, redirect
from django.db.models import Sum
from .forms import CriarVendedorForms
from .models import ListaVendedores
from vendas.models import Venda


def ver_todos_vendedores(request):
    ver_vendedores = ListaVendedores.objects.all()

    total_vendas_por_vendedor = {}

    for vendedor in ver_vendedores:
        total_vendas = (Venda.objects.filter(vendedor=vendedor.id).aggregate(total=Sum('valor'))['total'])

        total_vendas = total_vendas if total_vendas else 0

        total_vendas_por_vendedor[vendedor.nome] = total_vendas

    return render(request, 'listavendedorestodos.html', {'ver_vendedores': ver_vendedores, 'total_vendas_por_vendedor':total_vendas_por_vendedor})

def criar_vendedor(request):
    
    if request.method == 'POST':
        form = CriarVendedorForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vertodosvendedores')
        
    else:
        form = CriarVendedorForms()
    
    return render(request, 'vendedores_cadastrar.html', {'form': form})