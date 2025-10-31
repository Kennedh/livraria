"""
Crie uma classe abstrata Forma com método area().
Implemente Retangulo e Circulo que herdam dela e calculam suas áreas.
"""

from abc import ABC, abstractmethod

class Forma(ABC):

    @abstractmethod
    def area(self):
        pass

class Retangulo(Forma):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        print(f"Area do Retangulo: {(self.base * self.altura) / 2}")

class Circulo(Forma):

    def __init__(self, raio):
        self.raio = raio

    def area(self):
        #PI aproximado
        pi = 3.141592653589793
        print(f"Area do Circulo: {pi * (self.raio ** 2):.2f}")

# Teste

ret = Retangulo(8, 6)
ret.area()

circ = Circulo(5)
circ.area()
