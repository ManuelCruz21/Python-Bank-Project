import pytest
from models.conta import Conta

def test_criar_conta_inicializacao():
    conta = Conta("123", "Mané")
    assert conta.get_titular() == "Mané"
    assert conta.consultar_saldo() == 0
    assert conta.consultar_movimentos() == []

def test_criar_conta_com_valores_iniciais():
    movimentos_iniciais = [100, -20]
    conta = Conta("123", "Mané", saldo=80, movimentos=movimentos_iniciais)
    assert conta.consultar_saldo() == 80
    assert conta.consultar_movimentos() == [100, -20]

def test_depositar_sucesso():
    conta = Conta("123", "Mané", saldo=50)
    conta.depositar(100)
    assert conta.consultar_saldo() == 150
    assert 100 in conta.consultar_movimentos()

def test_depositar_valor_invalido():
    conta = Conta("123", "Mané")
    with pytest.raises(ValueError):
        conta.depositar(0)
    with pytest.raises(ValueError):
        conta.depositar(-50)

def test_levantar_sucesso():
    conta = Conta("123", "Mané", saldo=100)
    conta.levantar(40)
    assert conta.consultar_saldo() == 60
    assert -40 in conta.consultar_movimentos()

def test_levantar_valor_invalido():
    conta = Conta("123", "Mané", saldo=100)
    with pytest.raises(ValueError):
        conta.levantar(-10)

def test_levantar_saldo_insuficiente():
    conta = Conta("123", "Mané", saldo=30)
    with pytest.raises(ValueError):
        conta.levantar(50)

def test_transferir_sucesso():
    conta_origem = Conta("111", "Mané", saldo=200)
    conta_destino = Conta("222", "Ana", saldo=50)
    
    conta_origem.transferir(100, conta_destino)
    
    assert conta_origem.consultar_saldo() == 100
    assert conta_destino.consultar_saldo() == 150
    assert -100 in conta_origem.consultar_movimentos()

def test_transferir_valor_invalido():
    conta_origem = Conta("111", "Mané", saldo=200)
    conta_destino = Conta("222", "Ana", saldo=50)
    with pytest.raises(ValueError):
        conta_origem.transferir(-50, conta_destino)

def test_transferir_saldo_insuficiente():
    conta_origem = Conta("111", "Mané", saldo=20)
    conta_destino = Conta("222", "Ana", saldo=50)
    with pytest.raises(ValueError):
        conta_origem.transferir(100, conta_destino)