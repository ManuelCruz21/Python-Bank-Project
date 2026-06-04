from Conta import Conta

class Banco:

    def __init__(self, contas=None):
        self._contas = {} if contas is None else contas.copy()
        
    def criar_conta(self, numero, titular):
        if numero in self._contas:
            raise ValueError("Conta já existe.")
                        
        nova_conta = Conta(numero, titular, saldo=0, movimentos=[])
        self._contas[numero] = nova_conta
        
        return nova_conta
    
    def verifica_conta(self,numero):
        return numero in self._contas

    def remover_conta(self,numero):
        if self.verifica_conta(numero):
            del self._contas[numero]
            print("Conta removida.")
        else:
            print("Conta inexistente.")

    def procurar_conta(self, numero):
        if self.verifica_conta(numero):
            return self._contas[numero]
        else:
            raise ValueError("Conta não encontrada.")

    def listar_contas(self):
        for numero, conta in self._contas.items():
            print(f"{numero} - {conta._titular} - Saldo: {conta._saldo}")

