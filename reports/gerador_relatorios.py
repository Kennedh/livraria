from services.estoque_service import EstoqueService
from services.venda_service import VendaService

class GeradorRelatorios:
    def __init__(self, estoque_service: EstoqueService, venda_service: VendaService):
        self._estoque_service = estoque_service
        self._venda_service = venda_service

    def relatorio_estoque(self):
        return self._estoque_service.listar_estoque()

    def relatorio_vendas(self):
        if not self._venda_service._vendas:
            return "Nenhuma venda realizada"

        relatorio = "=== RELATÓRIO DE VENDAS ===\n"
        relatorio += "=" * 60 + "\n"
        
        for i, venda in enumerate(self._venda_service._vendas, 1):
            relatorio += f"\nVenda #{i}\n"
            relatorio += "-" * 40 + "\n"
            relatorio += venda.detalhes() + "\n"
            
            relatorio += "Itens:\n"
            for item in venda.itens:
                relatorio += (
                    f"  - {item.produto.titulo} | "
                    f"Qtd: {item.quantidade} | "
                    f"Unit: R$ {item.preco_unitario:.2f} | "
                    f"Subtotal: R$ {item.subtotal:.2f}\n"
                )
            
            relatorio += "-" * 40 + "\n"

        relatorio += "\n=== RESUMO FINANCEIRO ===\n"
        relatorio += f"Faturamento Total: R$ {self._venda_service.get_total_vendas():.2f}\n"
        relatorio += f"Lucro Bruto Total: R$ {self._venda_service.get_total_lucro():.2f}\n"
        relatorio += f"Margem de Lucro: {(self._venda_service.get_total_lucro() / self._venda_service.get_total_vendas() * 100):.2f}%\n"
        
        return relatorio

    def gerar_todos_relatorios(self):
        print(self.relatorio_estoque())
        print("\n")
        print(self.relatorio_vendas())