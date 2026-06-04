import pytest
from models.banco import Banco
from models.conta import Conta
from models.movimento import Movimento

def test_inicializar_banco_com_contas_pre_existentes():
    # 1. Criamos uma conta isolada para passar ao construtor
    conta_existente = Conta("99", "Pre-existente", saldo=100, movimentos=[])
    dicionario_contas = {"99": conta_existente}
    
    # 2. Inicializamos o Banco passando o dicionário (cobre o 'else' do __init__)
    banco = Banco(contas=dicionario_contas)
    assert banco.verifica_conta("99") is True

def test_criar_conta():
    banco = Banco()
    conta = banco.criar_conta("1", "Mané")
    assert conta.get_titular() == "Mané"
    assert conta.consultar_saldo() == 0
    assert banco.verifica_conta("1") is True

def test_conta_duplicada():
    banco = Banco()
    banco.criar_conta("1", "Mané")  
    with pytest.raises(ValueError):
        banco.criar_conta("1", "Outro")

def test_procurar_conta_com_sucesso():
    banco = Banco()
    banco.criar_conta("123", "Carlos")
    
    # Cobre o caminho "if" do procurar_conta
    conta_encontrada = banco.procurar_conta("123")
    assert conta_encontrada.get_titular() == "Carlos"

def test_procurar_conta_inexistente():
    banco = Banco()
    with pytest.raises(ValueError):
        banco.procurar_conta("999")

def test_remover_conta():
    banco = Banco()
    banco.criar_conta("1", "Mané")
    
    # Cobre o caminho "if" do remover_conta
    assert banco.remover_conta("1") is True
    assert banco.verifica_conta("1") is False

def test_remover_conta_inexistente():
    banco = Banco()
    with pytest.raises(ValueError):
        banco.remover_conta("999")

def test_listar_contas():
    banco = Banco()
    banco.criar_conta("1", "Mané")
    banco.criar_conta("2", "Ana")

    # Cobre a função listar_contas por completo
    contas_retornadas = banco.listar_contas()

    assert "1" in contas_retornadas
    assert "2" in contas_retornadas
    assert contas_retornadas["1"].get_titular() == "Mané"
    assert contas_retornadas["2"].get_titular() == "Ana"

def test_verifica_conta():
    banco = Banco()
    banco.criar_conta("1", "Mané")
    assert banco.verifica_conta("1") is True
    assert banco.verifica_conta("2") is False