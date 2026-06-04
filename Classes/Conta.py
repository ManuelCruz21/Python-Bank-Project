class Conta:

    def __init__(self,numero,titular,saldo,movimentos):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo
        self._movimentos = movimentos

    # Adiciona saldo à conta e regista um movimento.  
    def depositar(self,valor):
        self._saldo += valor
        self._movimentos.append(valor)

    # Retira saldo da conta (se houver saldo suficiente) e regista um movimento.
    def levantar(self,valor):
        if valor > self._saldo:
            print("Saldo insuficiente.")
        else:
            self._saldo -= valor
            self._movimentos.append(-valor)

    # Transfere valor para outra conta e regista um movimento.
    def transferir(self,valor,conta_destino):
        if valor > self._saldo:
            print("Saldo insuficiente.")
        else:
            self._saldo -= valor
            conta_destino.depositar(valor)
            self._movimentos.append(-valor)

    # Retorna o saldo atual da conta.
    def consultar_saldo(self):
        return self._saldo
    
    # Retorna a lista de movimentos da conta.
    def consultar_movimentos(self):
        return self._movimentos
    
    