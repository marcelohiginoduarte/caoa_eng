import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from lista_vendedores.models import ListaVendedores
from servico.models import Servico


@pytest.mark.django_db
def test_servico_models_criar_servico():
    vendedor = ListaVendedores.objects.create(nome='vendedor para test')

    fake_file = SimpleUploadedFile("dummy.txt", b"conteudo")

    servico = Servico.objects.create(
        cliente="Cliente Teste",
        telefone="1234567890",
        tipo_serviço="Eng_Solar",
        status="V",
        cidade="Cidade Teste",
        valor_empreendimento=1000.00,
        valor_custos=200.00,
        valor_lucro=800.00,
        email="teste@teste.com",
        mes="Janeiro",
        ano="2025",
        foto_documento=fake_file,
        comoprovante_endereco=fake_file,
        comoprovante_renda=fake_file,
        vendedor=vendedor,
        projeto_ativo=True,
    )

    assert servico.cliente == "Cliente Teste"
    assert servico.projeto_ativo is True


@pytest.mark.django_db
def test_servico_models_save_desativa_projeto_ativo_quando_status_concluido():
    vendedor = ListaVendedores.objects.create(nome='Vendedor Teste')

    fake_file = SimpleUploadedFile("dummy.txt", b"conteudo")

    servico = Servico.objects.create(
        cliente="Cliente Teste",
        telefone="1234567890",
        tipo_serviço="Eng_Solar",
        status="C",
        cidade="Cidade Teste",
        valor_empreendimento=1000.00,
        valor_custos=200.00,
        valor_lucro=800.00,
        email="teste@teste.com",
        mes="Janeiro",
        ano="2025",
        foto_documento=fake_file,
        comoprovante_endereco=fake_file,
        comoprovante_renda=fake_file,
        vendedor=vendedor,
        projeto_ativo=True,
    )

    servico.save()
    servico.refresh_from_db()
    assert servico.projeto_ativo is False


@pytest.mark.django_db
def test_servico_models_clean_valida_telefone():
    vendedor = ListaVendedores.objects.create(nome='Vendedor Teste')

    fake_file = SimpleUploadedFile("dummy.txt", b"conteudo")

    servico = Servico(
        cliente="Cliente Teste",
        telefone="telefone_invalido",
        tipo_serviço="Eng_Solar",
        status="V",
        cidade="Cidade Teste",
        valor_empreendimento=1000.00,
        valor_custos=200.00,
        valor_lucro=800.00,
        email="teste@teste.com",
        mes="Janeiro",
        ano="2025",
        foto_documento=fake_file,
        comoprovante_endereco=fake_file,
        comoprovante_renda=fake_file,
        vendedor=vendedor,
        projeto_ativo=True,
    )

    with pytest.raises(ValidationError):
        servico.clean()

@pytest.mark.django_db
def test_servico_models_str_retorna_nome_cliente():
    servico = Servico(cliente="Cliente Legal")
    assert str(servico) == "Cliente Legal"