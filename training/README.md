## 🚀 Meus Registros de Treino e Aprendizados

Esta seção é o meu diário de bordo durante a criação do projeto. Cada conceito de POO foi uma peça no quebra-cabeça.

* **Classes e Objetos (`__init__`, `self`):** Comecei modelando as classes mais simples, como `Autor` e `Cliente`. Foi um bom aquecimento para reforçar os fundamentos.

* **Herança (`Produto` -> `Livro`):** A ideia de ter uma classe `Produto` genérica e uma `Livro` que herda dela foi o que tornou o projeto "de verdade". Agora, se eu quiser vender canecas ou revistas, é só criar outra classe que herda de `Produto`. O sistema já está pronto pra isso.

* **Composição (`Livro` tem um `Autor`):** Entendi na prática a diferença entre "é um" (herança) e "tem um" (composição). Um `Livro` não é um `Autor`, ele *tem um*. O código ficou muito mais lógico assim.

* **Dunder Methods (`__eq__`, `__hash__`, `__str__`):** Essa parte foi um "click" na minha cabeça. Precisei usar `__eq__` e `__hash__` no `Produto` para poder usá-lo como chave no dicionário do estoque. Foi a primeira vez que vi uma utilidade tão clara para eles. O `__str__` também ajudou a deixar os relatórios bem mais legíveis.

* **Encapsulamento (`_itens` no Estoque):** Decidi deixar a lista de itens do estoque como "privada" (`_itens`). Isso me forçou a criar métodos para adicionar e remover itens, tornando o controle muito mais seguro e organizado.

* **Juntando Tudo:** A última etapa foi orquestrar tudo. Fazer a lógica de venda que primeiro checa o estoque, depois cria um objeto `Venda` e só então atualiza o estoque foi o maior desafio. Ver os relatórios de faturamento e lucro sendo gerados no final foi muito gratificante!
