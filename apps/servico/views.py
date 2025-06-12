from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from .forms import CadastrarServicoforms
from acompanhamentosfinanceiroprojeto.models import AcompanhamentoDespesasProjeto
from .models import Servico
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Case, When, Value, IntegerField


@login_required 
def home(request):
    return redirect('login')

@login_required
def entrada_principal(request):
    return render(request, 'servico_entrada.html')

def is_direcao(user):
    return user.groups.filter(name='direcao').exists()

@login_required
def dash_servico(request):
    if not request.user.groups.filter(name='direcao').exists():
            return render(request, 'sem_acesso.html')
    mes = [
    ('Janeiro', 'Jan'),
    ('Fevereiro', 'Fev'),
    ('Março', 'Mar'),
    ('Abril', 'Abr'),
    ('Maio', 'Mai'),
    ('Junho', 'Jun'),
    ('Julho', 'Jul'),
    ('Agosto', 'Ago'),
    ('Setembro', 'Set'),
    ('Outubro', 'Out'),
    ('Novembro', 'Nov'),
    ('Dezembro', 'Dez'),
]
    
    data_atual = now()
    mes_atual = mes[data_atual.month -1][0]
    ano_atual = str(data_atual.year)

    total_valor_vendido_mes = Servico.objects.filter(
        ano=ano_atual, 
        mes__iexact=mes_atual,
    ).aggregate(total=Sum('valor_empreendimento'))['total'] or 0

    total_valor_vendido = Servico.objects.aggregate(total=Sum('valor_empreendimento'))['total'] or 0

    contar_servicos_mes = Servico.objects.filter(ano=ano_atual, mes__iexact=mes_atual).count()
    contar_servicos_todos = Servico.objects.count()

    context = {'total_valor_vendido': total_valor_vendido,
            'total_valor_vendido_mes': total_valor_vendido_mes,
            'contar_servicos_mes': contar_servicos_mes,
            'contar_servicos_todos': contar_servicos_todos,
            }
    return render(request, 'home.html', context)


@login_required 
def cadastrar_servico(request):
    if not request.user.groups.filter(name='direcao').exists():
            return render(request, 'sem_acesso.html') 
    if request.method == 'POST':
        form = CadastrarServicoforms(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('todos_servicos') 
    else:
        form = CadastrarServicoforms()

    return render(request, 'servico_cadastrar.html', {'form': form})

@login_required 
def todos_servicos(request):
    if not request.user.groups.filter(name='direcao').exists():
        return render(request, 'sem_acesso.html')

    query = request.GET.get('q')
    mes_numero = request.GET.get('mes', '')
    ano = request.GET.get('ano', '')

    meses = [
        ('Janeiro', 'Jan'), ('Fevereiro', 'Fev'), ('Março', 'Mar'), ('Abril', 'Abr'),
        ('Maio', 'Mai'), ('Junho', 'Jun'), ('Julho', 'Jul'), ('Agosto', 'Ago'),
        ('Setembro', 'Set'), ('Outubro', 'Out'), ('Novembro', 'Nov'), ('Dezembro', 'Dez'),
    ]

    mes_nome = meses[int(mes_numero) - 1][0] if mes_numero else ''

    status_order = {
        'V': 0,
        'I': 1,
        'Co': 2,
        'A': 3,
        'E': 4,
        'P': 5,
        'C': 6,
    }

    ordenacao = Case(
        *[When(status=k, then=Value(v)) for k, v in status_order.items()],
        output_field=IntegerField()
    )

    todo_servico = Servico.objects.annotate(
        status_order=ordenacao
    ).order_by('status_order')

    if query:
        todo_servico = todo_servico.filter(cliente__icontains=query)
    if mes_nome:
        todo_servico = todo_servico.filter(mes=mes_nome)
    if ano:
        todo_servico = todo_servico.filter(ano=ano)

    paginator = Paginator(todo_servico, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    for sv in page_obj:
        total_custos = AcompanhamentoDespesasProjeto.objects.filter(projeto=sv).aggregate(
            total=Sum('valor')
        )['total'] or 0
        sv.valor_custos = total_custos

        if sv.valor_empreendimento:
            sv.porcentagem_custos = round((total_custos / sv.valor_empreendimento) * 100, 2)
            sv.valor_lucro = sv.valor_empreendimento - total_custos
        else:
            sv.porcentagem_custos = 0
            sv.valor_lucro = 0


    return render(request, 'servico_todos.html', {
        'page_obj': page_obj,
        'query': query,
        'mes': mes_numero,
        'ano': ano,
        'meses': list(enumerate(meses, start=1)),
    })

@login_required 
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


class DeletarServico(DeleteView):
    model = Servico
    template_name = 'servico__confirm_delete.html'
    success_url = reverse_lazy('todos_servicos')

@login_required
def detalhes_servico_json(request, id):
    ver_detalhe_servico = get_object_or_404(Servico, id=id)

    data = {
        'cliente': ver_detalhe_servico.cliente,
        'telefone': ver_detalhe_servico.telefone,
        'tipo_serviço': ver_detalhe_servico.tipo_serviço,
        'status': ver_detalhe_servico.status,
        'valor_empreendimento': ver_detalhe_servico.valor_empreendimento,
        'valor_custos': ver_detalhe_servico.valor_custos,
        'valor_lucro': ver_detalhe_servico.valor_lucro,
        'email': ver_detalhe_servico.email,
        'mes': ver_detalhe_servico.mes,
        'ano': ver_detalhe_servico.ano,
        'foto_documento': ver_detalhe_servico.foto_documento.url if ver_detalhe_servico.foto_documento else None,
        'comoprovante_endereco': ver_detalhe_servico.comoprovante_endereco.url if ver_detalhe_servico.comoprovante_endereco else None,
        'comoprovante_renda': ver_detalhe_servico.comoprovante_renda.url if ver_detalhe_servico.comoprovante_renda else None,
    }

    return JsonResponse(data)


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("entrada_do_sistema")
        else:
            messages.error(request, "Usuário ou senha incorretos")

    return render(request, "login.html")


def logout(request):
    logout(request)
    return redirect("login")


@login_required
def grafico_servico(request):
    servicos_por_mes = (Servico.objects.values('mes').annotate(total=Count('id')).order_by('mes'))

    meses = [
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
        "Jul", "Ago", "Set", "Out", "Nov", "Dez"
    ]
    dados = {mes: 0 for mes in meses}

    for servico in servicos_por_mes:
        dados[servico["mes"]] = servico["total"]

    contexto = {
        "labels": list(dados.keys()),  # Meses no eixo X
        "valores": list(dados.values()),  # Quantidade de serviços no eixo Y
    }

    return render(request, "home.html", contexto)