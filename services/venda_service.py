from datetime import datetime
from typing import Dict, List
from models.produto import Produto
from models.cliente import Cliente
from services.estoque_service import EstoqueService
from exceptions.custom_exceptions import VendaError

class ItemVenda:
    def __init__(self, produto: Produto, quantidade: int, preco_unitario: float):
        self.produto = produto
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.subtotal = preco_unitario * quantidade
        self.lucro_item = (preco_unitario - produto.custo) * quantidade

class Venda:
    def __init__(self, cliente: Cliente, itens: List[ItemVenda]):
        self._cliente = cliente
        self._itens = itens
        self._data = datetime.now()
        self._total = sum(item.subtotal for item in itens)
        self._lucro = sum(item.lucro_item for item in itens)

    @property
    def cliente(self):
        return self._cliente

    @property
    def itens(self):
        return self._itens.copy()

    @property
    def data(self):
        return self._data

    @property
    def total(self):
        return self._total

    @property
    def lucro(self):
        return self._lucro

    def detalhes(self):
        return (
            f"Data: {self._data.strftime('%d/%m/%Y %H:%M')}\n"
            f"Cliente: {self._cliente}\n"
            f"Itens: {len(self._itens)}\n"
            f"Total: R$ {self._total:.2f}\n"
            f"Lucro: R$ {self._lucro:.2f}"
        )

class VendaService:
    def __init__(self, estoque_service: EstoqueService):
        self._estoque_service = estoque_service
        self._vendas: List[Venda] = []

    def processar_venda(self, cliente: Cliente, carrinho: Dict[Produto, int]) -> Venda:
        """Processa uma venda validando estoque e criando registro"""
        if not carrinho:
            raise VendaError("Carrinho vazio")

        # Valida estoque para todos os itens
        for produto, quantidade in carrinho.items():
            disponivel = self._estoque_service.verificar_disponibilidade(produto)
            if quantidade > disponivel:
                raise VendaError(
                    f"Estoque insuficiente para {produto}. "
                    f"Disponível: {disponivel}, Solicitado: {quantidade}"
                )

        # Cria itens da venda e baixa estoque
        itens_venda = []
        for produto, quantidade in carrinho.items():
            itens_venda.append(ItemVenda(produto, quantidade, produto.preco_venda))
            self._estoque_service.remover_produto(produto, quantidade)

        venda = Venda(cliente, itens_venda)
        self._vendas.append(venda)
        return venda

    def get_total_vendas(self):
        return sum(venda.total for venda in self._vendas)

    def get_total_lucro(self):
        return sum(venda.lucro for venda in self._vendas)