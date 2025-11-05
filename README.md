# Projeto: Sistema de Gestão de Livraria em Python

Este é um projeto de console desenvolvido em Python como parte de um desafio para treinar Programação Orientada a Objetos (POO). O sistema simula a gestão de uma pequena livraria, controlando o estoque de produtos, registrando vendas e gerando relatórios financeiros básicos.

## Funcionalidades Principais

* **Gestão de Produtos:** Permite criar produtos com SKU, título, preço de venda e custo. O sistema é extensível, usando herança para criar tipos específicos de produtos, como `Livro`.
* **Controle de Estoque:** É possível adicionar, remover e verificar a quantidade de cada produto disponível.
* **Registro de Vendas:** Cada venda é registrada como uma transação única, guardando informações do cliente, os itens comprados, o valor total e o lucro gerado.
* **Geração de Relatórios:** O sistema pode exibir dois relatórios principais ao final da execução:
    1.  Um relatório de estoque atualizado.
    2.  Um relatório de vendas com o faturamento e o lucro bruto total.

##  Tecnologia Utilizada

* **Python 3**

1.  Certifique-se de ter o Python 3 instalado.
2.  Clone ou baixe os arquivos do projeto.
3.  Execute o arquivo principal pelo terminal:
    ```bash
    python nome_do_seu_arquivo.py
    ```
### Apesar do projeto ser voltado para livros, dá para adaptar para outros produtos apenas herdando a classe Produto

