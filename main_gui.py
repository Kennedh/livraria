import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from models.autor import Autor
from models.livro import Livro
from models.cliente import Cliente
from services.estoque_service import EstoqueService
from services.venda_service import VendaService
from reports.gerador_relatorios import GeradorRelatorios
from services.persistencia_service import PersistenciaService

class LivrariaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Sistema de Gestão de Livraria")
        self.root.geometry("1024x768")

        # Inicialização dos serviços
        self.estoque_service = EstoqueService()
        self.venda_service = VendaService(self.estoque_service)
        self.relatorios = GeradorRelatorios(self.estoque_service, self.venda_service)
        self.persistencia_service = PersistenciaService()  # NOVO

        self.autores = []
        self.livros = []
        self.clientes = []

        self.setup_ui()

        # Tentar carregar dados salvos
        if not self.persistencia_service.carregar_dados(self):
            # Se não houver dados salvos, carregar demo
            self.carregar_dados_demo()

        self.atualizar_todas_listas()

        # Configurar salvamento automático ao fechar
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def setup_ui(self):
        """Configura a interface gráfica"""
        # Frame superior com título
        frame_titulo = ttk.Frame(self.root)
        frame_titulo.pack(fill='x', padx=10, pady=5)
        ttk.Label(frame_titulo, text="📚 SISTEMA DE GESTÃO DE LIVRARIA",
                  font=('Arial', 16, 'bold')).pack(side='left')

        # Botões de persistência
        frame_persistencia = ttk.Frame(frame_titulo)
        frame_persistencia.pack(side='right')

        ttk.Button(frame_persistencia, text="💾 Salvar",
                   command=self.salvar_dados).pack(side='left', padx=2)
        ttk.Button(frame_persistencia, text="📂 Carregar",
                   command=self.carregar_dados).pack(side='left', padx=2)
        ttk.Button(frame_persistencia, text="📋 Backup",
                   command=self.fazer_backup).pack(side='left', padx=2)

        # Notebook (abas)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Criar abas
        self.tab_livros = ttk.Frame(self.notebook)
        self.tab_estoque = ttk.Frame(self.notebook)
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_vendas = ttk.Frame(self.notebook)
        self.tab_relatorios = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_livros, text='📖 Livros')
        self.notebook.add(self.tab_estoque, text='📦 Estoque')
        self.notebook.add(self.tab_clientes, text='👥 Clientes')
        self.notebook.add(self.tab_vendas, text='💰 Vendas')
        self.notebook.add(self.tab_relatorios, text='📊 Relatórios')

        # Configurar cada aba
        self.setup_tab_livros()
        self.setup_tab_estoque()
        self.setup_tab_clientes()
        self.setup_tab_vendas()
        self.setup_tab_relatorios()

    def setup_tab_livros(self):
        """Configura a aba de livros"""
        # Frame para cadastro
        frame_cadastro = ttk.LabelFrame(self.tab_livros, text="Cadastrar Novo Livro", padding=10)
        frame_cadastro.pack(fill='x', padx=10, pady=5)

        # Campos
        ttk.Label(frame_cadastro, text="SKU:").grid(row=0, column=0, sticky='w', padx=5)
        self.entry_sku = ttk.Entry(frame_cadastro, width=15)
        self.entry_sku.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_cadastro, text="Título:").grid(row=0, column=2, sticky='w', padx=5)
        self.entry_titulo = ttk.Entry(frame_cadastro, width=40)
        self.entry_titulo.grid(row=0, column=3, padx=5, pady=2)

        ttk.Label(frame_cadastro, text="Autor:").grid(row=1, column=0, sticky='w', padx=5)
        self.entry_autor_livro = ttk.Entry(frame_cadastro, width=20)
        self.entry_autor_livro.grid(row=1, column=1, padx=5, pady=2)

        ttk.Label(frame_cadastro, text="ISBN-10:").grid(row=1, column=2, sticky='w', padx=5)
        self.entry_isbn = ttk.Entry(frame_cadastro, width=20)
        self.entry_isbn.grid(row=1, column=3, padx=5, pady=2)

        ttk.Label(frame_cadastro, text="Preço Venda R$:").grid(row=2, column=0, sticky='w', padx=5)
        self.entry_preco = ttk.Entry(frame_cadastro, width=15)
        self.entry_preco.grid(row=2, column=1, padx=5, pady=2)

        ttk.Label(frame_cadastro, text="Preço Custo R$:").grid(row=2, column=2, sticky='w', padx=5)
        self.entry_custo = ttk.Entry(frame_cadastro, width=15)
        self.entry_custo.grid(row=2, column=3, padx=5, pady=2)

        frame_botoes = ttk.Frame(frame_cadastro)
        frame_botoes.grid(row=3, column=0, columnspan=4, pady=10)

        ttk.Button(frame_botoes, text="Cadastrar Livro",
                   command=self.cadastrar_livro).pack(side='left', padx=5)

        ttk.Button(frame_botoes, text="Excluir Livro",
                   command=self.excluir_livro).pack(side='left', padx=5)

        # Frame para listagem
        frame_lista = ttk.LabelFrame(self.tab_livros, text="Livros Cadastrados", padding=10)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=5)

        # Treeview
        self.tree_livros = ttk.Treeview(frame_lista,
                                        columns=('SKU', 'Título', 'Autor', 'Preço', 'Estoque'),
                                        show='headings')
        self.tree_livros.heading('SKU', text='SKU')
        self.tree_livros.heading('Título', text='Título')
        self.tree_livros.heading('Autor', text='Autor')
        self.tree_livros.heading('Preço', text='Preço')
        self.tree_livros.heading('Estoque', text='Estoque')

        self.tree_livros.column('SKU', width=80)
        self.tree_livros.column('Título', width=300)
        self.tree_livros.column('Autor', width=200)
        self.tree_livros.column('Preço', width=100)
        self.tree_livros.column('Estoque', width=100)

        self.tree_livros.pack(fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_livros.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_livros.configure(yscrollcommand=scrollbar.set)

    def setup_tab_estoque(self):
        """Configura a aba de estoque"""
        # Frame de controles
        frame_controles = ttk.Frame(self.tab_estoque)
        frame_controles.pack(fill='x', padx=10, pady=5)

        ttk.Button(frame_controles, text="Adicionar Estoque",
                   command=self.janela_adicionar_estoque).pack(side='left', padx=5)
        ttk.Button(frame_controles, text="Remover Estoque",
                   command=self.janela_remover_estoque).pack(side='left', padx=5)
        ttk.Button(frame_controles, text="Atualizar",
                   command=self.atualizar_lista_estoque).pack(side='left', padx=5)

        # Treeview do estoque
        frame_lista = ttk.Frame(self.tab_estoque)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree_estoque = ttk.Treeview(frame_lista,
                                         columns=('SKU', 'Produto', 'Qtd', 'V.Unit.', 'Total'),
                                         show='headings')
        self.tree_estoque.heading('SKU', text='SKU')
        self.tree_estoque.heading('Produto', text='Produto')
        self.tree_estoque.heading('Qtd', text='Qtd')
        self.tree_estoque.heading('V.Unit.', text='V.Unit.')
        self.tree_estoque.heading('Total', text='Total')

        self.tree_estoque.column('SKU', width=80)
        self.tree_estoque.column('Produto', width=400)
        self.tree_estoque.column('Qtd', width=80)
        self.tree_estoque.column('V.Unit.', width=100)
        self.tree_estoque.column('Total', width=100)

        self.tree_estoque.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_estoque.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_estoque.configure(yscrollcommand=scrollbar.set)

    def setup_tab_clientes(self):
        """Configura a aba de clientes"""
        # Frame de cadastro
        frame_cadastro = ttk.LabelFrame(self.tab_clientes, text="Cadastrar Cliente", padding=10)
        frame_cadastro.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky='w', padx=5)
        self.entry_nome_cliente = ttk.Entry(frame_cadastro, width=40)
        self.entry_nome_cliente.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(frame_cadastro, text="Email:").grid(row=1, column=0, sticky='w', padx=5)
        self.entry_email_cliente = ttk.Entry(frame_cadastro, width=40)
        self.entry_email_cliente.grid(row=1, column=1, padx=5, pady=2)

        ttk.Button(frame_cadastro, text="Cadastrar",
                   command=self.cadastrar_cliente).grid(row=2, column=0, columnspan=2, pady=10)

        # Lista de clientes
        frame_lista = ttk.Frame(self.tab_clientes)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree_clientes = ttk.Treeview(frame_lista,
                                          columns=('ID', 'Nome', 'Email'),
                                          show='headings')
        self.tree_clientes.heading('ID', text='ID')
        self.tree_clientes.heading('Nome', text='Nome')
        self.tree_clientes.heading('Email', text='Email')

        self.tree_clientes.column('ID', width=80)
        self.tree_clientes.column('Nome', width=300)
        self.tree_clientes.column('Email', width=300)

        self.tree_clientes.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_clientes.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)

    def setup_tab_vendas(self):
        """Configura a aba de vendas"""
        # Frame de controles
        frame_controles = ttk.Frame(self.tab_vendas)
        frame_controles.pack(fill='x', padx=10, pady=5)

        ttk.Button(frame_controles, text="Nova Venda",
                   command=self.janela_nova_venda).pack(side='left', padx=5)
        ttk.Button(frame_controles, text="Atualizar",
                   command=self.atualizar_lista_vendas).pack(side='left', padx=5)

        # Lista de vendas
        frame_lista = ttk.Frame(self.tab_vendas)
        frame_lista.pack(fill='both', expand=True, padx=10, pady=5)

        self.tree_vendas = ttk.Treeview(frame_lista,
                                        columns=('Data', 'Cliente', 'Itens', 'Total', 'Lucro'),
                                        show='headings')
        self.tree_vendas.heading('Data', text='Data')
        self.tree_vendas.heading('Cliente', text='Cliente')
        self.tree_vendas.heading('Itens', text='Itens')
        self.tree_vendas.heading('Total', text='Total')
        self.tree_vendas.heading('Lucro', text='Lucro')

        self.tree_vendas.column('Data', width=150)
        self.tree_vendas.column('Cliente', width=200)
        self.tree_vendas.column('Itens', width=100)
        self.tree_vendas.column('Total', width=100)
        self.tree_vendas.column('Lucro', width=100)

        self.tree_vendas.pack(fill='both', expand=True)

        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=self.tree_vendas.yview)
        scrollbar.pack(side='right', fill='y')
        self.tree_vendas.configure(yscrollcommand=scrollbar.set)

    def setup_tab_relatorios(self):
        """Configura a aba de relatórios"""
        frame_botoes = ttk.Frame(self.tab_relatorios)
        frame_botoes.pack(fill='x', padx=10, pady=5)

        ttk.Button(frame_botoes, text="Relatório de Estoque",
                   command=self.relatorio_estoque).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Relatório de Vendas",
                   command=self.relatorio_vendas).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Relatório Completo",
                   command=self.relatorio_completo).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Limpar",
                   command=self.limpar_relatorio).pack(side='left', padx=5)

        self.text_relatorio = scrolledtext.ScrolledText(self.tab_relatorios,
                                                        width=80, height=20,
                                                        font=('Courier', 10))
        self.text_relatorio.pack(fill='both', expand=True, padx=10, pady=5)

    def cadastrar_livro(self):
        """Cadastra um novo livro"""
        try:
            sku = self.entry_sku.get()
            titulo = self.entry_titulo.get()
            nome_autor = self.entry_autor_livro.get()
            isbn = self.entry_isbn.get()
            preco = float(self.entry_preco.get())
            custo = float(self.entry_custo.get())

            if not all([sku, titulo, nome_autor, isbn]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return

            # Criar ou buscar autor
            autor = next((a for a in self.autores if a.nome.lower() == nome_autor.lower()), None)
            if not autor:
                autor = Autor(nome_autor)
                self.autores.append(autor)

            livro = Livro(sku, titulo, preco, custo, autor, isbn)
            self.livros.append(livro)

            # Adicionar ao estoque com quantidade 0
            try:
                self.estoque_service.adicionar_produto(livro, 0)
            except:
                pass

            # Atualizar listas
            self.atualizar_lista_livros()
            self.atualizar_lista_estoque()

            # Limpar campos
            self.entry_sku.delete(0, tk.END)
            self.entry_titulo.delete(0, tk.END)
            self.entry_autor_livro.delete(0, tk.END)
            self.entry_isbn.delete(0, tk.END)
            self.entry_preco.delete(0, tk.END)
            self.entry_custo.delete(0, tk.END)

            messagebox.showinfo("Sucesso", f"Livro '{titulo}' cadastrado com sucesso!")

        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar livro: {e}")

    def cadastrar_cliente(self):
        """Cadastra um novo cliente"""
        nome = self.entry_nome_cliente.get()
        email = self.entry_email_cliente.get()

        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório!")
            return

        try:
            cliente = Cliente(nome, email if email else None)
            self.clientes.append(cliente)

            self.atualizar_lista_clientes()

            self.entry_nome_cliente.delete(0, tk.END)
            self.entry_email_cliente.delete(0, tk.END)

            messagebox.showinfo("Sucesso", f"Cliente '{nome}' cadastrado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def janela_adicionar_estoque(self):
        """Janela para adicionar estoque"""
        if not self.livros:
            messagebox.showwarning("Aviso", "Cadastre livros primeiro!")
            return

        janela = tk.Toplevel(self.root)
        janela.title("Adicionar ao Estoque")
        janela.geometry("400x200")

        ttk.Label(janela, text="Selecione o livro:").pack(pady=5)

        combo = ttk.Combobox(janela, values=[l.titulo for l in self.livros], width=40)
        combo.pack(pady=5)

        ttk.Label(janela, text="Quantidade:").pack(pady=5)
        entry_qtd = ttk.Entry(janela, width=20)
        entry_qtd.pack(pady=5)

        def adicionar():
            try:
                idx = combo.current()
                if idx < 0:
                    messagebox.showerror("Erro", "Selecione um livro!")
                    return

                qtd = int(entry_qtd.get())
                livro = self.livros[idx]
                self.estoque_service.adicionar_produto(livro, qtd)

                self.atualizar_lista_estoque()
                self.atualizar_lista_livros()

                messagebox.showinfo("Sucesso", f"{qtd} unidades adicionadas!")
                janela.destroy()
            except ValueError as e:
                messagebox.showerror("Erro", f"Valor inválido: {e}")

        ttk.Button(janela, text="Adicionar", command=adicionar).pack(pady=20)

    def janela_remover_estoque(self):
        """Janela para remover estoque"""
        if not self.livros:
            messagebox.showwarning("Aviso", "Cadastre livros primeiro!")
            return

        janela = tk.Toplevel(self.root)
        janela.title("Remover do Estoque")
        janela.geometry("400x200")

        ttk.Label(janela, text="Selecione o livro:").pack(pady=5)

        combo = ttk.Combobox(janela, values=[l.titulo for l in self.livros], width=40)
        combo.pack(pady=5)

        ttk.Label(janela, text="Quantidade:").pack(pady=5)
        entry_qtd = ttk.Entry(janela, width=20)
        entry_qtd.pack(pady=5)

        def remover():
            try:
                idx = combo.current()
                if idx < 0:
                    messagebox.showerror("Erro", "Selecione um livro!")
                    return

                qtd = int(entry_qtd.get())
                livro = self.livros[idx]
                self.estoque_service.remover_produto(livro, qtd)

                self.atualizar_lista_estoque()
                self.atualizar_lista_livros()

                messagebox.showinfo("Sucesso", f"{qtd} unidades removidas!")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        ttk.Button(janela, text="Remover", command=remover).pack(pady=20)

    def janela_nova_venda(self):
        """Janela para realizar nova venda"""
        if not self.clientes:
            messagebox.showwarning("Aviso", "Cadastre clientes primeiro!")
            return
        if not self.livros:
            messagebox.showwarning("Aviso", "Cadastre livros primeiro!")
            return

        janela = tk.Toplevel(self.root)
        janela.title("Nova Venda")
        janela.geometry("600x500")

        # Selecionar cliente
        ttk.Label(janela, text="Cliente:").pack(pady=5)
        combo_cliente = ttk.Combobox(janela, values=[c.nome for c in self.clientes], width=40)
        combo_cliente.pack(pady=5)

        # Carrinho
        ttk.Label(janela, text="Itens do Carrinho:").pack(pady=5)
        frame_carrinho = ttk.Frame(janela)
        frame_carrinho.pack(fill='both', expand=True, padx=10)

        tree_carrinho = ttk.Treeview(frame_carrinho, columns=('Livro', 'Qtd', 'Preço', 'Subtotal'), show='headings')
        tree_carrinho.heading('Livro', text='Livro')
        tree_carrinho.heading('Qtd', text='Qtd')
        tree_carrinho.heading('Preço', text='Preço Unit.')
        tree_carrinho.heading('Subtotal', text='Subtotal')
        tree_carrinho.pack(fill='both', expand=True)

        carrinho = {}

        def adicionar_item():
            if not self.livros:
                return

            item_janela = tk.Toplevel(janela)
            item_janela.title("Adicionar Item")
            item_janela.geometry("400x200")

            ttk.Label(item_janela, text="Livro:").pack(pady=5)
            combo_livro = ttk.Combobox(item_janela, values=[l.titulo for l in self.livros], width=40)
            combo_livro.pack(pady=5)

            ttk.Label(item_janela, text="Quantidade:").pack(pady=5)
            entry_qtd = ttk.Entry(item_janela, width=20)
            entry_qtd.pack(pady=5)

            def confirmar_item():
                try:
                    idx = combo_livro.current()
                    if idx < 0:
                        messagebox.showerror("Erro", "Selecione um livro!")
                        return

                    livro = self.livros[idx]
                    qtd = int(entry_qtd.get())

                    disponivel = self.estoque_service.verificar_disponibilidade(livro)
                    if qtd > disponivel:
                        messagebox.showerror("Erro", f"Estoque insuficiente! Disponível: {disponivel}")
                        return

                    carrinho[livro] = carrinho.get(livro, 0) + qtd

                    # Atualizar treeview
                    tree_carrinho.delete(*tree_carrinho.get_children())
                    total = 0
                    for l, q in carrinho.items():
                        subtotal = l.preco_venda * q
                        total += subtotal
                        tree_carrinho.insert('', 'end', values=(
                            l.titulo, q, f'R$ {l.preco_venda:.2f}', f'R$ {subtotal:.2f}'
                        ))

                    item_janela.destroy()
                except ValueError:
                    messagebox.showerror("Erro", "Quantidade inválida!")

            ttk.Button(item_janela, text="Adicionar", command=confirmar_item).pack(pady=20)

        def finalizar_venda():
            idx_cliente = combo_cliente.current()
            if idx_cliente < 0:
                messagebox.showerror("Erro", "Selecione um cliente!")
                return

            if not carrinho:
                messagebox.showerror("Erro", "Carrinho vazio!")
                return

            try:
                cliente = self.clientes[idx_cliente]
                venda = self.venda_service.processar_venda(cliente, carrinho)

                self.atualizar_lista_vendas()
                self.atualizar_lista_estoque()
                self.atualizar_lista_livros()

                messagebox.showinfo("Sucesso", f"Venda realizada! Total: R$ {venda.total:.2f}")
                janela.destroy()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

        frame_botoes = ttk.Frame(janela)
        frame_botoes.pack(pady=10)

        ttk.Button(frame_botoes, text="Adicionar Item", command=adicionar_item).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Finalizar Venda", command=finalizar_venda).pack(side='left', padx=5)

    def relatorio_estoque(self):
        """Exibe relatório de estoque"""
        self.limpar_relatorio()
        relatorio = self.relatorios.relatorio_estoque()
        self.text_relatorio.insert('1.0', relatorio)

    def relatorio_vendas(self):
        """Exibe relatório de vendas"""
        self.limpar_relatorio()
        relatorio = self.relatorios.relatorio_vendas()
        self.text_relatorio.insert('1.0', relatorio)

    def relatorio_completo(self):
        """Exibe relatório completo"""
        self.limpar_relatorio()
        relatorio_estoque = self.relatorios.relatorio_estoque()
        relatorio_vendas = self.relatorios.relatorio_vendas()
        self.text_relatorio.insert('1.0', relatorio_estoque + "\n\n" + relatorio_vendas)

    def limpar_relatorio(self):
        """Limpa o texto do relatório"""
        self.text_relatorio.delete('1.0', tk.END)

    def atualizar_todas_listas(self):
        """Atualiza todas as listas"""
        self.atualizar_lista_livros()
        self.atualizar_lista_estoque()
        self.atualizar_lista_clientes()
        self.atualizar_lista_vendas()

    def atualizar_lista_livros(self):
        """Atualiza a lista de livros"""
        self.tree_livros.delete(*self.tree_livros.get_children())
        for livro in self.livros:
            try:
                qtd = self.estoque_service.verificar_disponibilidade(livro)
            except:
                qtd = 0
            self.tree_livros.insert('', 'end', values=(
                livro.sku, livro.titulo, str(livro.autor),
                f'R$ {livro.preco_venda:.2f}', qtd
            ))

    def atualizar_lista_estoque(self):
        """Atualiza a lista de estoque"""
        self.tree_estoque.delete(*self.tree_estoque.get_children())
        for produto, qtd in self.estoque_service._estoque.items():
            self.tree_estoque.insert('', 'end', values=(
                produto.sku, str(produto), qtd,
                f'R$ {produto.preco_venda:.2f}',
                f'R$ {produto.preco_venda * qtd:.2f}'
            ))

    def atualizar_lista_clientes(self):
        """Atualiza a lista de clientes"""
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        for cliente in self.clientes:
            self.tree_clientes.insert('', 'end', values=(
                cliente.id, cliente.nome, cliente.email or '-'
            ))

    def atualizar_lista_vendas(self):
        """Atualiza a lista de vendas"""
        self.tree_vendas.delete(*self.tree_vendas.get_children())
        for venda in self.venda_service._vendas:
            self.tree_vendas.insert('', 'end', values=(
                venda.data.strftime('%d/%m/%Y %H:%M'),
                venda.cliente.nome,
                len(venda.itens),
                f'R$ {venda.total:.2f}',
                f'R$ {venda.lucro:.2f}'
            ))

    def carregar_dados_demo(self):
        """Carrega dados de demonstração"""
        try:
            autor1 = Autor("Machado de Assis")
            autor2 = Autor("Clarice Lispector")
            self.autores = [autor1, autor2]

            self.livros = [
                Livro("LIV001", "Dom Casmurro", 80.0, 65.0, autor1, "859431860X"),
                Livro("LIV002", "Quincas Borba", 79.50, 60.0, autor1, "8594318855"),
                Livro("LIV003", "A Hora da Estrela", 45.0, 30.0, autor2, "8532501012"),
            ]

            for livro, qtd in zip(self.livros, [40, 45, 30]):
                self.estoque_service.adicionar_produto(livro, qtd)

            self.clientes = [
                Cliente("Kennedh", "kennedh@email.com"),
                Cliente("Renan", "renan@email.com"),
            ]

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")

    def ao_fechar(self):
        """Executado quando a janela é fechada"""
        if messagebox.askyesno("Salvar Dados", "Deseja salvar os dados antes de sair?"):
            if self.persistencia_service.salvar_dados(self):
                messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar dados!")
        self.root.destroy()

    def salvar_dados(self):
        """Salva os dados manualmente"""
        if self.persistencia_service.salvar_dados(self):
            messagebox.showinfo("Sucesso", "✅ Dados salvos com sucesso!")
        else:
            messagebox.showerror("Erro", "❌ Erro ao salvar dados!")

    def carregar_dados(self):
        """Carrega dados salvos"""
        if messagebox.askyesno("Carregar Dados",
                               "Isso substituirá todos os dados atuais. Continuar?"):
            if self.persistencia_service.carregar_dados(self):
                self.atualizar_todas_listas()
                messagebox.showinfo("Sucesso", "✅ Dados carregados com sucesso!")
            else:
                messagebox.showinfo("Info", "📭 Nenhum dado encontrado ou erro ao carregar.")

    def fazer_backup(self):
        """Cria um backup dos dados"""
        sucesso, resultado = self.persistencia_service.fazer_backup(self)
        if sucesso:
            messagebox.showinfo("Backup", f"✅ Backup criado: {resultado}")
        else:
            messagebox.showerror("Erro", f"❌ Erro ao criar backup: {resultado}")

    def excluir_livro(self):
        """Exclui um livro que não tenha estoque"""

        # Verificar se existem livros cadastrados
        if not self.livros:
            messagebox.showwarning("Aviso", "📭 Nenhum livro cadastrado!")
            return

        # Criar janela de confirmação
        janela = tk.Toplevel(self.root)
        janela.title("Excluir Livro")
        janela.geometry("500x300")

        ttk.Label(janela, text="Selecione o livro para excluir:",
                  font=('Arial', 10)).pack(pady=10)

        # Mostrar apenas livros que podem ser excluídos (estoque = 0)
        ttk.Label(janela, text="📋 Livros sem estoque (disponíveis para exclusão):",
                  font=('Arial', 9, 'bold')).pack(pady=5)

        # Frame para lista
        frame_lista = ttk.Frame(janela)
        frame_lista.pack(fill='both', expand=True, padx=20, pady=10)

        # Treeview para mostrar livros
        tree = ttk.Treeview(frame_lista,
                            columns=('Título', 'Autor', 'SKU', 'Estoque', 'Status'),
                            show='headings',
                            height=8)

        tree.heading('Título', text='Título')
        tree.heading('Autor', text='Autor')
        tree.heading('SKU', text='SKU')
        tree.heading('Estoque', text='Estoque')
        tree.heading('Status', text='Status')

        tree.column('Título', width=200)
        tree.column('Autor', width=150)
        tree.column('SKU', width=80)
        tree.column('Estoque', width=80)
        tree.column('Status', width=100)

        tree.pack(fill='both', expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient='vertical', command=tree.yview)
        scrollbar.pack(side='right', fill='y')
        tree.configure(yscrollcommand=scrollbar.set)

        # Preencher lista com todos os livros
        livros_excluiveis = []
        livros_bloqueados = []

        for livro in self.livros:
            try:
                qtd = self.estoque_service.verificar_disponibilidade(livro)
            except:
                qtd = 0

            if qtd == 0:
                # Pode ser excluído
                status = "✅ Disponível"
                livros_excluiveis.append(livro)
                tree.insert('', 'end', values=(
                    livro.titulo, str(livro.autor), livro.sku, qtd, status
                ), tags=('disponivel',))
            else:
                # Não pode ser excluído
                status = "❌ Bloqueado"
                livros_bloqueados.append(livro)
                tree.insert('', 'end', values=(
                    livro.titulo, str(livro.autor), livro.sku, qtd, status
                ), tags=('bloqueado',))

        # Configurar cores
        tree.tag_configure('disponivel', background='#e8f5e8')  # Verde claro
        tree.tag_configure('bloqueado', background='#ffe8e8')  # Vermelho claro

        # Frame para botões
        frame_botoes = ttk.Frame(janela)
        frame_botoes.pack(pady=10)

        def confirmar_exclusao():
            """Confirma e executa a exclusão"""
            selecionado = tree.selection()

            if not selecionado:
                messagebox.showwarning("Aviso", "Selecione um livro para excluir!")
                return

            # Pegar o índice do item selecionado
            item = tree.item(selecionado[0])
            titulo = item['values'][0]

            # Encontrar o livro pelo título
            livro_encontrado = None
            for livro in self.livros:
                if livro.titulo == titulo:
                    livro_encontrado = livro
                    break

            if not livro_encontrado:
                messagebox.showerror("Erro", "Livro não encontrado!")
                return

            # Verificar estoque (dupla verificação)
            try:
                qtd = self.estoque_service.verificar_disponibilidade(livro_encontrado)
                if qtd > 0:
                    messagebox.showerror("Erro",
                                         f"❌ Não é possível excluir '{titulo}'!\n"
                                         f"Motivo: Ainda existem {qtd} unidades em estoque.\n"
                                         f"Remova todo o estoque primeiro.")
                    return
            except:
                pass  # Se der erro ao verificar, é porque não está no estoque

            # Confirmação final
            confirmar = messagebox.askyesno(
                "Confirmar Exclusão",
                f"⚠️ Tem certeza que deseja excluir permanentemente:\n\n"
                f"📖 {titulo}\n"
                f"✍️ {str(livro_encontrado.autor)}\n"
                f"🔖 SKU: {livro_encontrado.sku}\n\n"
                f"Esta ação não pode ser desfeita!"
            )

            if confirmar:
                # Remover o livro
                self.livros.remove(livro_encontrado)

                # Atualizar todas as listas
                self.atualizar_todas_listas()

                messagebox.showinfo("Sucesso", f"✅ Livro '{titulo}' excluído com sucesso!")
                janela.destroy()

        ttk.Button(frame_botoes, text="🗑️ Excluir Selecionado",
                   command=confirmar_exclusao).pack(side='left', padx=5)

        ttk.Button(frame_botoes, text="❌ Cancelar",
                   command=janela.destroy).pack(side='left', padx=5)

        # Label informativa
        if livros_bloqueados:
            ttk.Label(janela,
                      text=f"⚠️ {len(livros_bloqueados)} livro(s) bloqueado(s) - possuem estoque",
                      foreground='red').pack(pady=5)


def main():
    root = tk.Tk()
    app = LivrariaGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    exit(main())