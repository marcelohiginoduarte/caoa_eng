from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Count
from .forms import CadastrarServicoforms
from .models import Servico
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator


@login_required 
def home(request):
    return render(request, 'index.html')

@login_required
def dash_servico(request):

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

    print(f"Filtrando por Ano: {ano_atual}, Mês: {mes_atual}")
    total_valor_vendido_mes = Servico.objects.filter(
        ano=ano_atual, 
        mes__iexact=mes_atual,
    ).aggregate(total=Sum('valor_empreendimento'))['total'] or 0
    print(total_valor_vendido_mes)

    total_valor_vendido = Servico.objects.aggregate(total=Sum('valor_empreendimento'))['total'] or 0

    contar_servicos_mes = Servico.objects.filter(ano=ano_atual, mes__iexact=mes_atual).count()
    contar_servicos_todos = Servico.objects.count()

    context = {'total_valor_vendido': total_valor_vendido,
            'total_valor_vendido_mes': total_valor_vendido_mes,
            'contar_servicos_mes': contar_servicos_mes,
            'contar_servicos_todos': contar_servicos_todos,
            }
    return render(request, 'home.html', context)

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

    query = request.GET.get('q')
    mes_numero  = request.GET.get('mes', '') #precisei fazer isso, por que a pesquisa estava sendo por numero.
    ano = request.GET.get('ano', '')

    meses = [
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


    if mes_numero:
        mes_nome = meses[int(mes_numero) - 1][0]
    else:
        mes_nome = ''

    todo_servico = Servico.objects.all().order_by('id')

    if query:
        todo_servico = todo_servico.filter(cliente__icontains=query)

    if mes_nome:
        todo_servico = todo_servico.filter(mes=mes_nome)

    if ano:
        todo_servico = todo_servico.filter(ano=ano)

    paginator = Paginator(todo_servico, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'servico_todos.html', {'page_obj': page_obj, 'query': query, 'mes': mes_nome, 'ano': ano})


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
            return redirect("login.html")
        else:
            messages.error(request, "Usuário ou senha incorretos")

    return render(request, "login.html")


def logout(request):
    logout(request)
    return redirect("login")