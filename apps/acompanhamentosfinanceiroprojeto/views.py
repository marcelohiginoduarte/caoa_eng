from django.shortcuts import render, redirect
from .models import AcompanhamentoDespesasProjeto
from .forms import CriarAcompanhamentoDespesasForms
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from servico.models import Servico
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy


@login_required
def criar_despesa_projeto(request):
    if not request.user.groups.filter(name='direcao').exists():
        return request(request, 'sem_acesso.html')
    if request.method == 'POST':
        form = CriarAcompanhamentoDespesasForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('criardespesaprojetotodas')
    else:
        form = CriarAcompanhamentoDespesasForms()

    return render(request, 'criar_despesa_projeto.html', {'form': form})

@login_required
def ver_despesas_projeto(request):
    if not request.user.groups.filter(name='direcao').exists():
        return request(request, 'sem_acesso.html')
    projeto_filtro = request.GET.get('projeto', '') 
    projetos = Servico.objects.all()  
    custos = AcompanhamentoDespesasProjeto.objects.all()  
    
    if projeto_filtro:
        projeto_selecionado = Servico.objects.filter(cliente=projeto_filtro).first()
        if projeto_selecionado:
            custos = custos.filter(projeto=projeto_selecionado) 
            valor_empreendimento = projeto_selecionado.valor_empreendimento
            total_valor = custos.aggregate(total=Sum('valor'))['total'] or 0 
            
            if valor_empreendimento > 0:
                porcentagem = (total_valor / valor_empreendimento) * 100
                saldo_restante = valor_empreendimento - total_valor
            else:
                porcentagem = 0
                saldo_restante = valor_empreendimento
        else:
            total_valor = 0
            porcentagem = 0
            saldo_restante = 0
    else:
        total_valor = custos.aggregate(total=Sum('valor'))['total'] or 0
        porcentagem = 0
        saldo_restante = 0

    return render(request, 'despesas_todas.html', {
        'custos': custos,
        'total_valor': total_valor,
        'projetos': projetos,
        'projeto_filtro': projeto_filtro,
        'porcentagem': porcentagem,
        'saldo_restante': saldo_restante,
    })



class AtualizarCustos(UpdateView):
    model = AcompanhamentoDespesasProjeto
    template_name = 'custos_atualizar.html'
    form_class = CriarAcompanhamentoDespesasForms
    success_url = reverse_lazy('criardespesaprojetotodas')


class DeletarCustos(DeleteView):
    model = AcompanhamentoDespesasProjeto
    template_name = 'custos__confirm_delete.html'
    success_url = reverse_lazy('criardespesaprojetotodas')