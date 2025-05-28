import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from servico.models import Servico
from lista_vendedores.models import ListaVendedores


@pytest.mark.django_db
def test_servico_url_dash_servico(client):
    response = client.get(reverse('dash_servico'))
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_servico_url_cadastrar_servico(client):
    response = client.get(reverse('cadastrar_servicos'))
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_servico_url_servico_url_editar_servico_view(client):
    vendedor = ListaVendedores.objects.create(nome="Teste")
    servico = Servico.objects.create(
        cliente="Cliente Teste",
        telefone="1234567890",
        tipo_serviço="Eng_Solar",
        status="V",
        cidade="Cidade Teste",
        valor_empreendimento=1000,
        valor_custos=500,
        valor_lucro=500,
        email="teste@teste.com",
        mes="Janeiro",
        ano="2025",
        vendedor=vendedor,
    )
    url = reverse('editar_servico', args=[servico.id])
    response = client.get(url)
    assert response.status_code in [200, 302]


@pytest.mark.django_db
def test_servico_url_detalhes_servico_json_view(client):
    vendedor = ListaVendedores.objects.create(nome="Teste")
    servico = Servico.objects.create(
        cliente="Cliente JSON",
        telefone="1234567890",
        tipo_serviço="Eng_Solar",
        status="V",
        cidade="Cidade Teste",
        valor_empreendimento=1000,
        valor_custos=500,
        valor_lucro=500,
        email="teste@teste.com",
        mes="Janeiro",
        ano="2025",
        vendedor=vendedor,
    )
    url = reverse('detalhe_servico', args=[servico.id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'


@pytest.mark.django_db
def test_logout_view(client):
    User.objects.create_user(username='marceloteste', password='teste123')
    client.login(username='marceloteste', password='teste123')
    response = client.post(reverse('logout'))
    assert response.status_code in [200, 302]