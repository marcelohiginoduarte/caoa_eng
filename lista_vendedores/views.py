from django.shortcuts import render, redirect
from .forms import CriarVendedorForms
from .models import ListaVendedores


def ver_todos_vendedores(request):
    ver_vendedores = ListaVendedores.objects.all()
    return render(request, 'listavendedorestodos.html', {'ver_vendedores': ver_vendedores})

def criar_vendedor(request):
    
    if request.method == 'POST':
        form = CriarVendedorForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vertodosvendedores')
        
    else:
        form = CriarVendedorForms()
    
    return render(request, 'vendedores_cadastrar.html', {'form': form})