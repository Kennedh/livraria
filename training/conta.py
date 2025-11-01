"""
Crie uma classe Conta com atributo privado _saldo.
Use @property para exibir e @setter para atualizar com validação (saldo não negativo).

"""

class Conta:

    def __init__(self, titular, saldo_inicial=0):
        self.titular = titular
        self.__saldo = saldo_inicial

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, valor):
        if valor < 0:
            raise ValueError("Saldo aceita apenas valores positivos")
        else:
            self.__saldo = valor

# Teste

cc = Conta("Kennedh")

print(cc.saldo)

cc.saldo = 600

print(cc.saldo)