from datetime import datetime

class Produto:
    def __init__(self, sku, titulo, preco_venda, custo):
        self.sku = sku
        self.titulo = titulo
        self.preco_venda = preco_venda
        self.custo = custo

class Autor:
    def __init__(self, nome):
        self.nome = nome

    def __str__(self):
        return self.nome

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
        self.isbn = isbn # ISBN-10

    # Para retornar valor sobre o objeto no print()
    def detalhes(self):
         print(f"SKU: {self.sku} Titulo: {self.titulo} \nPreço de Venda: R$ {self.preco_venda} Preço de Custo: R$ {self.custo}\n"
                f"Autor: {self.autor}\n"
                f"ISBN-10: {self.isbn}")

    def __str__(self):
        return self.titulo

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

    def adicionar_estoque(self, produto, qt):
        if produto not in self.estoque:
            self.estoque[produto] = qt
            print(f"Livro {produto} cadastrado e adicionado {qt} ao estoque.")
        else:
            self.estoque[produto] += qt
            print(f"Adicionado mais {qt} ao {produto} no estoque.")

    def verificar_disponibilidade(self, produto):
        if produto not in self.estoque:
            print("Produto não cadastrado")
        print(f"Saldo atual: {self.estoque[produto]}")

    def diminuir_estoque(self, produto, qt):
        if produto not in self.estoque:
            print("Produto não cadastrado")
        if qt > self.estoque[produto]:
            print("Saldo em estoque inferior ao solicitado.")
        else:
            self.estoque[livro1] -= qt
            print(f"Retirado {qt} unidades do estoque do {livro1}\n\n"
                  f"Novo saldo: {self.estoque[produto]}")

    def estoque_completo(self):
        for produto, qt in self.estoque.items():
            print(f"Produto: {produto} Saldo: {qt}")

    def processar_venda(self, cliente, carrinho):
        print(f"\n--- Iniciando processamento da venda para {cliente.nome} ---")

        try:
            for item, qt in carrinho.items():
                if item not in self.estoque:
                    raise ValueError(f"Produto {item} não cadastrado.")
                if qt > self.estoque[item]:
                    raise ValueError(
                        f"Estoque insuficiente para {item}. Pedido: {qt}, Disponível: {self.estoque[item]}")

            print("Validação de estoque: OK.")

        except ValueError as e:
            print(f"Falha ao processar venda: {e}")
            return None

        print("Executando baixa no estoque...")
        for item, qt in carrinho.items():
            self.diminuir_estoque(item, qt)

        # 3. Cria e retorna o "recibo"
        print("Venda concluída com sucesso!")
        return Venda(cliente, carrinho)

class Cliente:
    _contador_id = 0

    def __init__(self, nome):
        self.nome = nome

        # Auto incrementação de ID de modo basico
        Cliente._contador_id += 1
        self.id_cliente = Cliente._contador_id

    def __str__(self):
        return f"ID: {self.id_cliente} Nome: {self.nome}"

class Venda:
    def __init__(self, cliente, carrinho):
        self.cliente = cliente
        self.carrinho = carrinho

        self.total_venda = 0
        self.lucro_total = 0
        self.hora_venda  = datetime.now()

        for item, qt in self.carrinho.items():
            self.total_venda += item.preco_venda * qt
            self.lucro_total += (item.preco_venda * qt) - (item.custo * qt)


# Teste

autor1 = Autor("Machado de Assis")
livro1 = Livro("001","Dom Casmurro", 80.0, 65, autor1, "859431860X")
livro2 = Livro("001", "Quincas Borba", 79.50, 60, autor1, "8594318855")

livro1.detalhes()

estoque = Estoque()

estoque.adicionar_estoque(livro1, 40)
estoque.adicionar_estoque(livro2, 45)

estoque.verificar_disponibilidade(livro1)
estoque.diminuir_estoque(livro1, 20)

estoque.estoque_completo()

c1 = Cliente("Kennedh")
c2 = Cliente("Renan")

print(c1)
print(c2)

venda1 = estoque.processar_venda(c1, {livro1:6, livro2:5})

print(venda1.lucro_total)