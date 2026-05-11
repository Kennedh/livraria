from models.autor import Autor
from models.livro import Livro
from models.cliente import Cliente
from services.estoque_service import EstoqueService
from services.venda_service import VendaService
from reports.gerador_relatorios import GeradorRelatorios

def main():
    print("=" * 60)
    print("SISTEMA DE GESTÃO DE LIVRARIA".center(60))
    print("=" * 60)

    # Inicialização dos serviços
    estoque_service = EstoqueService()
    venda_service = VendaService(estoque_service)
    relatorios = GeradorRelatorios(estoque_service, venda_service)

    try:
        # Cadastro de autores
        print("\n>>> Cadastrando autores...")
        autor1 = Autor("Machado de Assis")
        autor2 = Autor("Clarice Lispector")
        
        # Cadastro de livros
        print(">>> Cadastrando livros...")
        livros = [
            Livro("LIV001", "Dom Casmurro", 80.0, 65.0, autor1, "859431860X"),
            Livro("LIV002", "Quincas Borba", 79.50, 60.0, autor1, "8594318855"),
            Livro("LIV003", "A Hora da Estrela", 45.0, 30.0, autor2, "8532501012"),
            Livro("LIV004", "Memórias Póstumas", 65.0, 45.0, autor1, "8532501013"),
        ]
        
        # Exibe detalhes dos livros
        for livro in livros:
            print(f"\n{livro.detalhes()}")
            print("-" * 40)

        # Adiciona ao estoque
        print("\n>>> Abastecendo estoque...")
        quantidades_iniciais = [40, 45, 30, 35]
        for livro, qtd in zip(livros, quantidades_iniciais):
            estoque_service.adicionar_produto(livro, qtd)
            print(f"✓ {livro.titulo}: {qtd} unidades")

        # Cadastro de clientes
        print("\n>>> Cadastrando clientes...")
        clientes = [
            Cliente("Kennedh", "kennedh@email.com"),
            Cliente("Renan", "renan@email.com"),
        ]
        
        for cliente in clientes:
            print(f"✓ {cliente}")

        # Processamento de vendas
        print("\n>>> Processando vendas...")
        
        # Venda 1
        carrinho1 = {
            livros[0]: 6,
            livros[1]: 5
        }
        venda1 = venda_service.processar_venda(clientes[0], carrinho1)
        print(f"✓ Venda #1 concluída - Total: R$ {venda1.total:.2f}")
        
        # Venda 2
        carrinho2 = {
            livros[0]: 8,
            livros[1]: 10,
            livros[2]: 3
        }
        venda2 = venda_service.processar_venda(clientes[1], carrinho2)
        print(f"✓ Venda #2 concluída - Total: R$ {venda2.total:.2f}")

        # Tratamento de erro - tentativa de venda com estoque insuficiente
        print("\n>>> Testando validação de estoque...")
        try:
            carrinho3 = {livros[0]: 100}  # Quantidade maior que disponível
            venda_service.processar_venda(clientes[0], carrinho3)
        except Exception as e:
            print(f"✗ Erro esperado: {e}")

        # Geração de relatórios finais
        print("\n")
        relatorios.gerar_todos_relatorios()

    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())