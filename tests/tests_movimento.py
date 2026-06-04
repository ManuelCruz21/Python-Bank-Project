from datetime import datetime
from models.movimento import Movimento

def test_criar_movimento_basico():
    mov = Movimento(tipo="Depósito", valor=50.0)
    
    assert mov._tipo == "Depósito"
    assert mov._valor == 50.0
    assert mov._descricao == ""
    assert mov._conta_destino is None
    assert isinstance(mov._data, datetime)

def test_criar_movimento_completo():
    mov = Movimento(
        tipo="Transferência", 
        valor=100.0, 
        descricao="Prenda de anos", 
        conta_destino="987654"
    )
    
    assert mov._tipo == "Transferência"
    assert mov._valor == 100.0
    assert mov._descricao == "Prenda de anos"
    assert mov._conta_destino == "987654"

def test_str_movimento_sem_destino():
    mov = Movimento(tipo="Levantamento", valor=20.0, descricao="Multibanco")
    
    resultado_str = str(mov)
    
    assert "Levantamento" in resultado_str
    assert "20.0" in resultado_str
    assert "Multibanco" in resultado_str
    assert "->" not in resultado_str 

def test_str_movimento_com_destino():
    mov = Movimento(
        tipo="Transferência", 
        valor=150.0, 
        descricao="Renda", 
        conta_destino="12345"
    )
    
    resultado_str = str(mov)
    
    assert "Transferência" in resultado_str
    assert "150.0" in resultado_str
    assert "-> 12345" in resultado_str
    assert "Renda" in resultado_str