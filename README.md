# Sistema de Gestão de Livraria

> Aplicação desktop em Python para controle de livros, estoque, clientes, vendas e relatórios, estruturada com Programação Orientada a Objetos.

O projeto simula um sistema interno de gestão para uma livraria e concentra regras de negócio, persistência de dados e interface gráfica em uma aplicação organizada em diferentes módulos.

## 🎯 O problema que resolve

Mesmo uma operação pequena precisa controlar informações como:

- produtos cadastrados;
- quantidade disponível;
- clientes;
- vendas realizadas;
- custos e margens;
- histórico de movimentações;
- relatórios.

O sistema reúne essas rotinas em uma aplicação única e aplica validações para evitar inconsistências no fluxo.

## ✨ Principais funcionalidades

### 📚 Produtos
- Cadastro de livros
- SKU único
- Título, custo e preço de venda
- Validação de valores
- Cálculo de margem
- Associação com autores
- Validação de ISBN-10

### 📦 Estoque
- Entrada de produtos
- Remoção de unidades
- Consulta de disponibilidade
- Atualização após vendas
- Cálculo do valor total em estoque
- Regras para impedir operações inválidas

### 🛒 Vendas
- Carrinho com múltiplos itens
- Validação de estoque
- Cálculo de subtotais
- Cálculo de lucro por item
- Registro de data e hora
- Histórico de transações

### 👥 Clientes
- Cadastro de clientes
- Identificador automático
- Dados de contato
- Consulta por ID

### 📊 Relatórios
- Relatório de estoque
- Relatório de vendas
- Visão consolidada da operação
- Exibição organizada dos dados

### 💾 Persistência
- Carregamento automático dos dados
- Salvamento manual
- Salvamento ao encerrar
- Backup com timestamp
- Dados persistidos em JSON

### 🛡️ Validação e tratamento de erros
- Exceções customizadas
- Validações de regras de negócio
- Mensagens de erro descritivas
- Alertas visuais

## 🧱 Organização do projeto

```text
livraria/
├── exceptions/     # exceções de negócio
├── models/         # entidades e modelos
├── reports/        # geração de relatórios
├── services/       # regras e serviços da aplicação
├── training/       # materiais e experimentações do desenvolvimento
├── main_gui.py     # interface e ponto de entrada
└── README.md
```

A separação em módulos ajuda a manter responsabilidades distintas e facilita a evolução do sistema.

## 🛠️ Tecnologias e conceitos

- Python 3
- Tkinter / ttk
- Programação Orientada a Objetos
- JSON
- Tratamento de exceções
- Separação de responsabilidades
- Regras de negócio
- Persistência local de dados

## ▶️ Como executar

Clone o repositório:

```bash
git clone https://github.com/Kennedh/livraria.git
cd livraria
```

Execute a interface:

```bash
python main_gui.py
```

> O Tkinter normalmente acompanha as instalações padrão do Python para Windows e macOS. Em algumas distribuições Linux pode ser necessário instalar o pacote correspondente do Tkinter.

## 💡 O que este projeto demonstra

Mais do que uma tela de cadastro, o projeto trabalha com situações comuns em sistemas empresariais:

- validação de dados;
- regras de estoque;
- consistência entre venda e quantidade disponível;
- organização por entidades e serviços;
- persistência;
- geração de informações para acompanhamento da operação.

## 🚀 Possíveis evoluções

- Migração da persistência de JSON para banco de dados
- Autenticação e níveis de acesso
- Busca e filtros avançados
- Exportação de relatórios
- Dashboard com indicadores
- Testes automatizados
- Empacotamento como aplicação instalável

---

Desenvolvido por [Kennedh](https://github.com/Kennedh).
