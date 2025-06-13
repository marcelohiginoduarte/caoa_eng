from django.shortcuts import render, redirect
from .models import AcompanhamentoDespesasProjeto
from .forms import CriarAcompanhamentoDespesasForms
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.mixins import LoginRequiredMixin
from servico.models import Servico
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from concurrent.futures import ProcessPoolExecutor
from django.http import FileResponse
from datetime import datetime
import zipfile
import tempfile
import os
from django.conf import settings


@login_required
def criar_despesa_projeto(request):
    if not request.user.groups.filter(name='direcao').exists():
        return request(request, 'sem_acesso.html')
    if request.method == 'POST':
        form = CriarAcompanhamentoDespesasForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('criardespesaprojeto')
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


class AtualizarCustos(LoginRequiredMixin, UpdateView):
    model = AcompanhamentoDespesasProjeto
    template_name = 'custos_atualizar.html'
    form_class = CriarAcompanhamentoDespesasForms
    success_url = reverse_lazy('criardespesaprojetotodas')
    login_url = 'login'

class DeletarCustos(LoginRequiredMixin, DeleteView):
    model = AcompanhamentoDespesasProjeto
    template_name = 'custos__confirm_delete.html'
    success_url = reverse_lazy('criardespesaprojetotodas')
    login_url = 'login'


@login_required
def gerar_relatorio(request):
    projeto_filtro = request.GET.get('projeto', None)

    if projeto_filtro:
        custos = AcompanhamentoDespesasProjeto.objects.filter(projeto__cliente=projeto_filtro)
    else:
        custos = AcompanhamentoDespesasProjeto.objects.all()

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=100, bottomMargin=50)

    elements = []
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        name='Titulo',
        parent=styles['Title'],
        fontSize=16,
        alignment=1,
        textColor=colors.HexColor('#003366'),
        spaceAfter=10
    )

    logo_path = os.path.join('media', 'logo_caoa.png')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=120, height=50)
        img.hAlign = 'LEFT'
        elements.append(img)

    elements.append(Paragraph("Relatório de Custos Operacionais", titulo_style))
    elements.append(Paragraph(f"<b>Empresa:</b> Caoa Engenharia", styles['Normal']))
    if projeto_filtro:
        elements.append(Paragraph(f"<b>Projeto:</b> {projeto_filtro}", styles['Normal']))
    elements.append(Paragraph(f"<b>Data:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    data = [['Projeto', 'Descrição', 'Valor', 'Data Compra', 'Observação']]
    for custo in custos:
        data.append([
            custo.projeto.cliente,
            custo.descricao,
            f'R$ {custo.valor:,.2f}',
            custo.data_compra.strftime('%d/%m/%Y'),
            custo.observacao or '-'
        ])

    table = Table(data, hAlign='CENTER', colWidths=[100, 130, 80, 90, 130])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f2f2f2")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (2, 1), (2, -1), 'RIGHT'),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ])

    table.setStyle(style)
    elements.append(table)

    def add_page_number(canvas, doc):
        page_num_text = f"Página {doc.page}"
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        canvas.drawString(500, 15, page_num_text)
        canvas.restoreState()

    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    nome_projeto = projeto_filtro if projeto_filtro else 'todos_projetos'
    nome_arquivo = f'Caoaeng_{nome_projeto}.pdf'.replace(' ', '_')
    response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    return response


@login_required
def gerar_pdf_por_projeto(cliente):
    from django.db import connection
    connection.close()

    custos = AcompanhamentoDespesasProjeto.objects.filter(projeto__cliente=cliente)

    temp_path = os.path.join(settings.MEDIA_ROOT, f"temp_pdfs/{cliente.replace(' ', '_')}.pdf")
    os.makedirs(os.path.dirname(temp_path), exist_ok=True)

    doc = SimpleDocTemplate(temp_path, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    titulo_style = ParagraphStyle(
        name='Titulo',
        parent=styles['Title'],
        fontSize=16,
        alignment=1,
        textColor=colors.HexColor('#003366'),
        spaceAfter=10
    )

    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo_caoa.png')
    if os.path.exists(logo_path):
        img = Image(logo_path, width=120, height=50)
        img.hAlign = 'LEFT'
        elements.append(img)

    elements.append(Paragraph("Relatório de Custos Operacionais", titulo_style))
    elements.append(Paragraph(f"<b>Projeto:</b> {cliente}", styles['Normal']))
    elements.append(Paragraph(f"<b>Data:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    data = [['Descrição', 'Valor', 'Data Compra', 'Observação']]
    for custo in custos:
        data.append([
            custo.descricao,
            f'R$ {custo.valor:,.2f}',
            custo.data_compra.strftime('%d/%m/%Y'),
            custo.observacao or '-'
        ])

    table = Table(data, hAlign='CENTER', colWidths=[130, 80, 90, 130])
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f2f2f2")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ])
    table.setStyle(style)
    elements.append(table)

    doc.build(elements)
    return temp_path


@csrf_exempt
def gerar_varios_pdfs_zip(request):
    projetos = AcompanhamentoDespesasProjeto.objects.values_list('projeto__cliente', flat=True).distinct()

    with tempfile.TemporaryDirectory() as temp_dir:
        pdf_dir = os.path.join(temp_dir, "pdfs")
        os.makedirs(pdf_dir, exist_ok=True)

        def wrapper(cliente):
            path = gerar_pdf_por_projeto(cliente)
            return path

        with ProcessPoolExecutor() as executor:
            resultados = list(executor.map(wrapper, projetos))

        zip_path = os.path.join(temp_dir, "relatorios.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for pdf_path in resultados:
                if os.path.exists(pdf_path):
                    zipf.write(pdf_path, arcname=os.path.basename(pdf_path))

        return FileResponse(open(zip_path, 'rb'), as_attachment=True, filename="relatorios.zip")
