"""
Crie uma classe Animal com método falar().
Crie Cachorro e Gato que herdam de Animal e sobrescrevem falar().
Faça uma lista com ambos e chame falar() de cada.
"""

class Animal:
    def __init__(self, nome):
        self.nome = nome

    def falar(self):
        print("Grrrrrrr")

class Cachorro(Animal):
    def falar(self):
        print("Au au")

class Gato(Animal):
    def falar(self):
        print("Miau")

# Teste

dog = Cachorro("Tôtó")
cat = Gato("Pelota")

dog.falar()
cat.falar()

print(dog.nome)
print(cat.nome)