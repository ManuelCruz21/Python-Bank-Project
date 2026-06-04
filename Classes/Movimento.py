from datetime import datetime

class Movimento:

    def __init__(self, tipo, valor, descricao="", conta_destino=None):
        self._tipo = tipo
        self._valor = valor
        self._data = datetime.now()
        self._descricao = descricao
        self._conta_destino = conta_destino

    def __str__(self):
        destino = f" -> {self._conta_destino}" if self._conta_destino else ""
        return (
            f"{self._data} | {self._tipo} | {self._valor}"
            f"{destino} | {self._descricao}"
        )