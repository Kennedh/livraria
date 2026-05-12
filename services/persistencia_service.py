import json
import os
from datetime import datetime
from models.autor import Autor
from models.livro import Livro
from models.cliente import Cliente
from services.estoque_service import EstoqueService
from services.venda_service import VendaService, Venda, ItemVenda

class PersistenciaService:
    """Serviço para salvar e carregar dados do sistema"""

    def __init__(self, arquivo_dados="dados_livraria.json"):
        self.arquivo_dados = arquivo_dados

    def salvar_dados(self, app):
        """Salva todos os dados da aplicação"""
        dados = {
            'autores': [],
            'livros': [],
            'estoque': [],
            'clientes': [],
            'vendas': [],
            'contador_cliente': Cliente._contador_id
        }

        # Salvar autores
        for autor in app.autores:
            dados['autores'].append({
                'nome': autor.nome
            })

        # Salvar livros
        for livro in app.livros:
            dados['livros'].append({
                'sku': livro.sku,
                'titulo': livro.titulo,
                'preco_venda': livro.preco_venda,
                'custo': livro.custo,
                'autor_nome': livro.autor.nome,
                'isbn': livro.isbn
            })

        # Salvar estoque
        for produto, quantidade in app.estoque_service._estoque.items():
            dados['estoque'].append({
                'sku': produto.sku,
                'quantidade': quantidade
            })

        # Salvar clientes
        for cliente in app.clientes:
            dados['clientes'].append({
                'id': cliente.id,
                'nome': cliente.nome,
                'email': cliente.email
            })

        # Salvar vendas
        for venda in app.venda_service._vendas:
            itens = []
            for item in venda.itens:
                itens.append({
                    'sku': item.produto.sku,
                    'quantidade': item.quantidade,
                    'preco_unitario': item.preco_unitario
                })

            dados['vendas'].append({
                'cliente_id': venda.cliente.id,
                'data': venda.data.isoformat(),
                'itens': itens
            })

        # Salvar em arquivo
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False

    def carregar_dados(self, app):
        """Carrega os dados salvos para a aplicação"""
        if not os.path.exists(self.arquivo_dados):
            print("Arquivo de dados não encontrado. Iniciando com dados vazios.")
            return False

        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            # Limpar dados atuais
            app.autores.clear()
            app.livros.clear()
            app.clientes.clear()
            app.estoque_service._estoque.clear()
            app.venda_service._vendas.clear()

            # Carregar autores
            autores_dict = {}
            for autor_dados in dados.get('autores', []):
                autor = Autor(autor_dados['nome'])
                app.autores.append(autor)
                autores_dict[autor.nome] = autor

            # Carregar livros
            livros_dict = {}
            for livro_dados in dados.get('livros', []):
                autor = autores_dict.get(livro_dados['autor_nome'])
                if autor:
                    livro = Livro(
                        livro_dados['sku'],
                        livro_dados['titulo'],
                        livro_dados['preco_venda'],
                        livro_dados['custo'],
                        autor,
                        livro_dados['isbn']
                    )
                    app.livros.append(livro)
                    livros_dict[livro.sku] = livro

            # Carregar estoque
            for estoque_dados in dados.get('estoque', []):
                livro = livros_dict.get(estoque_dados['sku'])
                if livro:
                    app.estoque_service.adicionar_produto(
                        livro,
                        estoque_dados['quantidade']
                    )

            # Carregar clientes
            clientes_dict = {}
            for cliente_dados in dados.get('clientes', []):
                cliente = Cliente(
                    cliente_dados['nome'],
                    cliente_dados.get('email')
                )
                # Restaurar ID original
                cliente._id = cliente_dados['id']
                app.clientes.append(cliente)
                clientes_dict[cliente.id] = cliente

            # Restaurar contador de clientes
            if dados.get('contador_cliente'):
                Cliente._contador_id = dados['contador_cliente']

            # Carregar vendas
            for venda_dados in dados.get('vendas', []):
                cliente = clientes_dict.get(venda_dados['cliente_id'])
                if cliente:
                    carrinho = {}
                    for item_dados in venda_dados['itens']:
                        livro = livros_dict.get(item_dados['sku'])
                        if livro:
                            carrinho[livro] = item_dados['quantidade']

                    if carrinho:
                        # Criar venda diretamente (sem processar, pois estoque já está ajustado)
                        itens_venda = []
                        for produto, quantidade in carrinho.items():
                            itens_venda.append(
                                ItemVenda(produto, quantidade, produto.preco_venda)
                            )

                        venda = Venda(cliente, itens_venda)
                        venda._data = datetime.fromisoformat(venda_dados['data'])
                        app.venda_service._vendas.append(venda)

            return True

        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False

    def fazer_backup(self, app):
        """Cria um backup dos dados atuais"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_backup = f"backup_livraria_{timestamp}.json"

        try:
            self.arquivo_dados = arquivo_backup
            self.salvar_dados(app)
            self.arquivo_dados = "dados_livraria.json"  # Restaurar nome original
            return True, arquivo_backup
        except Exception as e:
            return False, str(e)