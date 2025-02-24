from django.shortcuts import render, redirect
from .models import AcompanhamentoDespesasProjeto
from .forms import CriarAcompanhamentoDespesasForms
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from servico.models import Servico
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors



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


def gerar_relatorio(request):
    projeto_filtro = request.GET.get('projeto', None)
    
    if projeto_filtro:
        custos = AcompanhamentoDespesasProjeto.objects.filter(projeto__cliente=projeto_filtro)
    else:
        custos = AcompanhamentoDespesasProjeto.objects.all()
    
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)

    data = [['Projeto', 'Descrição', 'Valor', 'Data Compra', 'Observação']]
    
    for custo in custos:
        data.append([
            custo.projeto.cliente, 
            custo.descricao, 
            f'{custo.valor:,.2f}',
            custo.data_compra.strftime('%d/%m/%Y'),  
            custo.observacao or '-'
        ])

    table = Table(data)

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('ALIGN', (1, 1), (-1, -1), 'LEFT'),
    ])
    table.setStyle(style)

    doc.build([table])

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_custos.pdf"'
    return response
