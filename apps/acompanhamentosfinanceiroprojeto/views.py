from django.shortcuts import render, redirect
from .models import AcompanhamentoDespesasProjeto
from .forms import CriarAcompanhamentoDespesasForms
from django.contrib.auth.decorators import login_required


@login_required
def criar_despesa_projeto(request):
    if not request.user.groups.filter(name='direcao').exists():
        return request(request, 'sem_acesso.html')
    if request.method == 'POST':
        form = CriarAcompanhamentoDespesasForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Acompanhardespesas')
    else:
        form = CriarAcompanhamentoDespesasForms()

    return render(request, 'criar_despesa_projeto.html', {'form': form})
