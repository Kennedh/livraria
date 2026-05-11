from models.produto import Produto
from models.autor import Autor
import re

class Livro(Produto):
    def __init__(self, sku: str, titulo: str, preco_venda: float, 
                 custo: float, autor: Autor, isbn: str):
        super().__init__(sku, titulo, preco_venda, custo)
        self._validar_isbn(isbn)
        self._autor = autor
        self._isbn = isbn

    @property
    def autor(self):
        return self._autor

    @property
    def isbn(self):
        return self._isbn

    def __str__(self):
        return f"{self._titulo} - {self._autor}"

    def __eq__(self, other):
        if isinstance(other, Livro):
            return (self._titulo.lower() == other._titulo.lower() and 
                   self._autor == other._autor)
        return False

    def __hash__(self):
        return hash((self._titulo.lower(), self._autor))

    def detalhes(self):
        detalhes_base = super().detalhes()
        return (
            f"{detalhes_base}\n"
            f"Autor: {self._autor}\n"
            f"ISBN-10: {self._isbn}"
        )

    def _validar_isbn(self, isbn):
        """Valida formato ISBN-10"""
        if not re.match(r'^\d{9}[\dX]$', isbn):
            raise ValueError(f"ISBN-10 inválido: {isbn}")