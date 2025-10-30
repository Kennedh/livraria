"""
Crie uma classe Produto com nome e preco.
Implemente __str__ para mostrar o produto de forma bonita.
Implemente __add__ para somar preços de dois produtos.

"""

class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco
    def __str__(self):
        return f"Produto: {self.nome} | Preço: R$ {self.preco}"
    def __add__(self, obj):
        if not isinstance(obj, Produto):
            return NotImplemented
        preco_total = self.preco + obj.preco
        return f"Preço total dos Produtos\nValor: R$ {preco_total}"


# Teste

pao = Produto("Pão Francês", 4.5)

print(pao)

queijo = Produto("Queijo Mussarela", 5)

print(pao + queijo)
