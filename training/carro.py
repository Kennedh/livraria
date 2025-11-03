"""Crie uma classe Motor e uma classe Carro que possui um motor.
Quando o carro for ligado, chame o método ligar() do motor.
"""

class Motor:
    def ligar(self):
        print("Motor ligado")

class Carro:
    def __init__(self, marca, modelo):
        self.motor = Motor()
        self.marca = marca
        self.modelo = modelo

    def ligar(self):
        print("Ligando carro...")
        self.motor.ligar()


# Teste

motor = Motor()
carro = Carro("Citroen", "C3")

carro.ligar()