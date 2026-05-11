from typing import Dict
from models.produto import Produto
from exceptions.custom_exceptions import (
    ProdutoNaoCadastradoError,
    EstoqueInsuficienteError
)

class EstoqueService:
    def __init__(self):
        self._estoque: Dict[Produto, int] = {}
        self._log = []

    @property
    def estoque(self):
        return self._estoque.copy()

    def adicionar_produto(self, produto: Produto, quantidade: int):
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        
        if produto not in self._estoque:
            self._estoque[produto] = quantidade
            self._log.append(f"Produto {produto} cadastrado com {quantidade} unidades")
        else:
            self._estoque[produto] += quantidade
            self._log.append(f"Adicionadas {quantidade} unidades de {produto}")
        
        return self._estoque[produto]

    def remover_produto(self, produto: Produto, quantidade: int):
        if produto not in self._estoque:
            raise ProdutoNaoCadastradoError(f"Produto {produto} não encontrado")
        
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        
        if quantidade > self._estoque[produto]:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente para {produto}. "
                f"Disponível: {self._estoque[produto]}, "
                f"Solicitado: {quantidade}"
            )
        
        self._estoque[produto] -= quantidade
        
        if self._estoque[produto] == 0:
            del self._estoque[produto]
        
        self._log.append(f"Removidas {quantidade} unidades de {produto}")

    def verificar_disponibilidade(self, produto: Produto) -> int:
        if produto not in self._estoque:
            raise ProdutoNaoCadastradoError(f"Produto {produto} não cadastrado")
        return self._estoque[produto]

    def listar_estoque(self) -> str:
        if not self._estoque:
            return "Estoque vazio"
        
        relatorio = "=== RELATÓRIO DE ESTOQUE ===\n"
        relatorio += f"{'SKU':<10} {'Produto':<40} {'Qtd':<5} {'Valor Unit.':<12} {'Total':<12}\n"
        relatorio += "-" * 80 + "\n"
        
        for produto, quantidade in self._estoque.items():
            relatorio += (
                f"{produto.sku:<10} "
                f"{str(produto):<40} "
                f"{quantidade:<5} "
                f"R$ {produto.preco_venda:<11.2f} "
                f"R$ {produto.preco_venda * quantidade:<11.2f}\n"
            )
        
        return relatorio

    def get_log(self):
        return self._log.copy()