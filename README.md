# 📚 Sistema de Gestão de Livraria

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow.svg)

Sistema de console desenvolvido em Python para gestão completa de uma livraria, utilizando Programação Orientada a Objetos (POO). O sistema oferece controle de estoque, registro de vendas, gestão de clientes e geração de relatórios financeiros detalhados.

## 📑 Índice

- [Funcionalidades](#-funcionalidades)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Diagrama de Classes](#-diagrama-de-classes)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Execução](#-instalação-e-execução)
- [Como Usar](#-como-usar)
- [Exemplos de Código](#-exemplos-de-código)
- [Testes](#-testes)
- [Extensibilidade](#-extensibilidade)
- [Boas Práticas Implementadas](#-boas-práticas-implementadas)
- [Possíveis Melhorias Futuras](#-possíveis-melhorias-futuras)
- [Contribuição](#-contribuição)
- [Licença](#-licença)
- [Contato](#-contato)

## ✨ Funcionalidades

### 📦 Gestão de Produtos
- Cadastro de produtos com SKU único, título, preço de venda e custo
- Validação de preços (não podem ser negativos e venda >= custo)
- Cálculo automático de margem de lucro
- Suporte a diferentes tipos de produtos via herança
- ISBN-10 com validação de formato para livros

### 🏪 Controle de Estoque
- Adição de novos produtos ao estoque
- Remoção de produtos com validação de quantidade
- Consulta de disponibilidade por produto
- Listagem completa do estoque com valor total
- Tratamento de erros para estoque insuficiente

### 💰 Registro de Vendas
- Processamento de vendas com múltiplos itens
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
- **Resumo Financeiro**: faturamento total, lucro bruto e margem percentual
- Formatação profissional com tabelas alinhadas

### 🛡️ Tratamento de Erros
- Exceções customizadas para erros de negócio
- Validações de entrada em todos os métodos
- Mensagens de erro descritivas
