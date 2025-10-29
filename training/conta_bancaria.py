"""
Crie uma classe ContaBancaria com métodos:
depositar()
sacar() (não permitir saldo negativo)
exibir_saldo()
Simule uma sequência de depósitos e saques.

"""

class ContaBancaria:
    def __init__(self):
        self.saldo = 0

    def depositar(self, valor):
        self.saldo += valor
        print(f"Deposito realizado no valor de R$ {valor}")

    def sacar(self, valor):
        if valor > self.saldo:
            print(f"Valor de saque superior ao saldo atual: R$ {self.saldo}")
        else:
            self.saldo -= valor
            print(f"Novo Saldo: R$ {self.saldo}")

    def exibir_saldo(self):
        print(f"Saldo Atual: R$ {self.saldo}")

# Teste

minha_conta = ContaBancaria()

minha_conta.exibir_saldo()

minha_conta.depositar(6.5)

minha_conta.exibir_saldo()

minha_conta.sacar(8)