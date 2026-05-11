from abc import ABC, abstractmethod

class Produto(ABC):
    def __init__(self, sku: str, titulo: str, preco_venda: float, custo: float):
        self._validar_precos(preco_venda, custo)
        self._sku = sku
        self._titulo = titulo
        self._preco_venda = preco_venda
        self._custo = custo

    @property
    def sku(self):
        return self._sku

    @property
    def titulo(self):
        return self._titulo

    @property
    def preco_venda(self):
        return self._preco_venda

    @preco_venda.setter
    def preco_venda(self, valor):
        if valor < 0:
            raise ValueError("Preço de venda não pode ser negativo")
        self._preco_venda = valor

    @property
    def custo(self):
        return self._custo

    @custo.setter
    def custo(self, valor):
        if valor < 0:
            raise ValueError("Custo não pode ser negativo")
        self._custo = valor

    @property
    def margem_lucro(self):
        return self._preco_venda - self._custo

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    def _validar_precos(self, preco_venda, custo):
        if preco_venda < 0 or custo < 0:
            raise ValueError("Preços não podem ser negativos")
        if preco_venda < custo:
            raise ValueError("Preço de venda não pode ser menor que o custo")

    def detalhes(self):
        return (
            f"SKU: {self._sku} | Título: {self._titulo}\n"
            f"Preço de Venda: R$ {self._preco_venda:.2f} | "
            f"Preço de Custo: R$ {self._custo:.2f}\n"
            f"Margem de Lucro: R$ {self.margem_lucro:.2f}"
        )