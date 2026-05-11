class EstoqueError(Exception):
    """Exceção base para erros de estoque"""
    pass

class ProdutoNaoCadastradoError(EstoqueError):
    """Produto não encontrado no estoque"""
    pass

class EstoqueInsuficienteError(EstoqueError):
    """Quantidade solicitada maior que disponível"""
    pass

class VendaError(Exception):
    """Exceção base para erros de venda"""
    pass