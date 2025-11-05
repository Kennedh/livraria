class Produto:
    def __init__(self, sku, titulo, preco_venda, custo):
        self.sku = sku
        self.titulo = titulo
        self.preco_venda = preco_venda
        self.custo = custo

class Autor:
    def __init__(self, nome):
        self.nome = nome

    # Diferenciação entre autores
    def __eq__(self, other):
        if isinstance(other, Autor):
            return self.nome == other.nome
        return False

    #Implementação para estoque
    def __hash__(self):
        return hash(self.nome)

class Livro(Produto):
    def __init__(self, sku, titulo, preco_venda, custo, autor, isbn):
        super().__init__(sku, titulo, preco_venda, custo)
        self.autor = autor
        self.isbn = isbn

    # Comparação entre livros, quando nome e autor for igual
    def __eq__(self, other):
        if isinstance(other, Livro):
            return self.titulo == other.titulo and self.autor == other.autor
        return False

    # Para armazenar no estoque via dicionário
    def __hash__(self):
        return hash((self.titulo, self.autor))

class Estoque:
    def __init__(self):
        self.estoque = {}

    def adicionar_estoque(self, obj_livro, qt):
        if obj_livro not in self.estoque:
            self.estoque[obj_livro] = qt
            print(f"Livro {obj_livro} adicionado ao estoque.")

