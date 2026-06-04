class Movimento:

    def __init__(self, tipo, valor, data, descricao,conta_destino):
        self._tipo = tipo
        self._valor = valor
        self._data = data
        self._descricao = descricao
        self._conta_destino = conta_destino

    def __str__(self):
        return f"Tipo: {self._tipo}, Valor: {self._valor}, Data: {self._data}, Descrição: {self._descricao}, Conta Destino: {self._conta_destino}"
    

