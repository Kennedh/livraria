# 📚 Sistema de Gestão de Livraria

Sistema desenvolvido em Python para gestão completa de uma livraria, utilizando Programação Orientada a Objetos (POO).

O sistema oferece controle de estoque, registro de vendas, gestão de clientes, geração de relatórios financeiros e **persistência de dados em JSON**.

## ✨ Funcionalidades

### 📦 Gestão de Produtos
- Cadastro de livros com SKU único, título, preço de venda e custo
- Validação de preços (não podem ser negativos e venda >= custo)
- Cálculo automático de margem de lucro
- Suporte a diferentes tipos de produtos via herança
- ISBN-10 com validação de formato para livros
- Associação com autores (cadastro automático)

### 🏪 Controle de Estoque
- Adição de novos produtos ao estoque
- Remoção de produtos com validação de quantidade
- Consulta de disponibilidade por produto
- Listagem completa do estoque com valor total
- Atualização automática após vendas

### 💰 Registro de Vendas
- Processamento de vendas com múltiplos itens
- Carrinho de compras dinâmico
- Validação de estoque antes da conclusão
- Cálculo automático de subtotais e lucro por item
- Registro de data/hora de cada venda
- Histórico completo de transações

### 👥 Gestão de Clientes
- Cadastro de clientes com ID automático
- Suporte a informações de contato (email)
- Identificação única por ID

### 📊 Relatórios
- **Relatório de Estoque**: produtos, quantidades, valores unitários e totais
- **Relatório de Vendas**: detalhamento de cada transação
- **Relatório Completo**: visão geral do negócio
- Formatação profissional com tabelas alinhadas

### 💾 Persistência de Dados
- Salvamento automático ao fechar o programa
- Salvamento manual quando desejar
- Carga automática de dados ao iniciar
- Sistema de backup com timestamp
- Dados armazenados em formato JSON

### 🛡️ Tratamento de Erros
- Exceções customizadas para erros de negócio
- Validações de entrada em todos os campos
- Mensagens de erro descritivas
- Alertas visuais na interface gráfica
