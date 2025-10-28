"""Crie uma classe Pessoa com atributos nome e idade.
Adicione um método falar() que imprime uma frase usando os atributos.
Instancie duas pessoas e chame o método.
"""

class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def falar(self):
        print(f"Olá, meu nome é {self.nome} e tenho {self.idade}")

# Teste

p1 = Pessoa("Kennedh",29)

p1.falar()

