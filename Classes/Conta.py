class Conta:

    def __init__(self, numero, titular, saldo=0, movimentos=None):
        self.__numero = numero
        self.__titular = titular
        self.__saldo = saldo
        self.__movimentos = movimentos if movimentos is not None else []

    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor inválido.")

        self.__saldo += valor
        self.__movimentos.append(valor)

    def levantar(self, valor):
        if valor <= 0:
            raise ValueError("Valor inválido.")

        if valor > self.__saldo:
            raise ValueError("Saldo insuficiente.")

        self.__saldo -= valor
        self.__movimentos.append(-valor)

    def transferir(self, valor, conta_destino):
        if valor <= 0:
            raise ValueError("Valor inválido.")

        if valor > self.__saldo:
            raise ValueError("Saldo insuficiente.")

        self.__saldo -= valor
        conta_destino.depositar(valor)
        self.__movimentos.append(-valor)

    def consultar_saldo(self):
        return self.__saldo

    def consultar_movimentos(self):
        return self.__movimentos
    
    def get_titular(self):
        return self.__titular