from django.shortcuts import render, redirect, get_object_or_404
from .forms import CadastrarServicoforms
from .models import Servico

def home(request):
    return render(request, 'index.html')

def dash_servico(request):
    return render(request, 'home.html')

def cadastrar_servico(request):
    
    if request.method == 'POST':
        form = CadastrarServicoforms(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('todos_servicos') 
    else:
        form = CadastrarServicoforms()

    return render(request, 'servico_cadastrar.html', {'form': form})

def todos_servicos(request):
    todo_servico = Servico.objects.all()
    return render(request, 'servico_todos.html', {'todo_servico': todo_servico})


def editar_servico(request, servico_id):
    servico = get_object_or_404(Servico, id=servico_id)
    if request.method == 'POST':
        form = CadastrarServicoforms(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            return redirect ('todos_servicos')
    else:
        form = CadastrarServicoforms(instance=servico)
    return render(request, 'servico_editar.html', {'form': form})