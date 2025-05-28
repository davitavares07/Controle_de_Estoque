import tkinter as tk
from tkinter import ttk, messagebox
from dados_banco import (
    Produto,
    adicionar_novo_produto,
    atualizar_produto_existente,
    excluir_produto_por_indice
)

class CadastroProdutosTab(ttk.Frame):
    def __init__(self, parent, produtos_cadastrados_ref, update_listbox_callback):
        super().__init__(parent)
        # O 'parent' é o ttk.Notebook, não a janela principal
        # Recebemos a referência à lista de produtos e a função de callback
        self.produtos_cadastrados = produtos_cadastrados_ref
        self.update_listbox_callback = update_listbox_callback

        self.indice_selecionado = None
        self.create_widgets()

    def create_widgets(self):
        # Configuração de grid para esta aba (Frame)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # --- Frame Esquerdo: Formulário de Cadastro/Edição ---
        cadastro_frame = ttk.LabelFrame(self, text="Cadastrar/Editar Produto", padding="15")
        cadastro_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        cadastro_frame.grid_columnconfigure(0, weight=0)
        cadastro_frame.grid_columnconfigure(1, weight=1)

        # Labels e Entradas
        ttk.Label(cadastro_frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.nome_entry = ttk.Entry(cadastro_frame)
        self.nome_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)
        self.nome_entry.bind("<Return>", self.cadastrar_produto_via_event)

        ttk.Label(cadastro_frame, text="Preço (R$):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.preco_entry = ttk.Entry(cadastro_frame)
        self.preco_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=5)
        self.preco_entry.bind("<Return>", self.cadastrar_produto_via_event)

        ttk.Label(cadastro_frame, text="Quantidade:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.quantidade_entry = ttk.Entry(cadastro_frame)
        self.quantidade_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=5)
        self.quantidade_entry.bind("<Return>", self.cadastrar_produto_via_event)

        # Botão Cadastrar/Salvar
        self.cadastrar_button = ttk.Button(cadastro_frame, text="Cadastrar", command=self.cadastrar_produto)
        self.cadastrar_button.grid(row=3, column=0, columnspan=2, pady=15)

        # Botão Cancelar Edição
        self.cancelar_button = ttk.Button(cadastro_frame, text="Cancelar Edição", command=self.cancelar_edicao)

        # --- Frame Direito: Lista de Produtos ---
        lista_frame = ttk.LabelFrame(self, text="Produtos Cadastrados", padding="15")
        lista_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        lista_frame.grid_rowconfigure(0, weight=1)
        lista_frame.grid_columnconfigure(0, weight=1)

        # Listbox para exibir os produtos
        self.produtos_listbox = tk.Listbox(lista_frame, height=15)
        self.produtos_listbox.grid(row=0, column=0, sticky="nsew")
        self.produtos_listbox.bind("<Double-Button-1>", self.carregar_para_edicao)

        # Adicionar Scrollbar para a Listbox
        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.produtos_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.produtos_listbox.config(yscrollcommand=scrollbar.set)

        # Botão de Excluir
        excluir_button = ttk.Button(lista_frame, text="Excluir Selecionado", command=self.excluir_produto)
        excluir_button.grid(row=1, column=0, columnspan=2, pady=10)

    def atualizar_listbox(self):
        """Atualiza a Listbox desta aba com os dados da lista de produtos."""
        self.produtos_listbox.delete(0, tk.END)
        for produto in self.produtos_cadastrados:
            self.produtos_listbox.insert(tk.END, str(produto))

    def cadastrar_produto_via_event(self, event=None):
        self.cadastrar_produto()

    def cadastrar_produto(self):
        nome = self.nome_entry.get().strip()
        preco_str = self.preco_entry.get().strip()
        quantidade_str = self.quantidade_entry.get().strip()

        if not nome or not preco_str or not quantidade_str:
            messagebox.showwarning("Campos Vazios", "Todos os campos devem ser preenchido.")
            return

        try:
            preco = float(preco_str)
            if preco < 0:
                messagebox.showerror("Erro de Preço", "O preço não pode ser negativo.")
                return

            quantidade = int(quantidade_str)
            if quantidade < 0:
                messagebox.showerror("Erro de Quantidade", "A quantidade não pode ser negativa.")
                return

        except ValueError:
            messagebox.showerror("Erro de Entrada", "Preço deve ser um número e Quantidade um número inteiro.")
            return

        if self.indice_selecionado is None:
            adicionar_novo_produto(self.produtos_cadastrados, nome, preco, quantidade)
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
        else:
            atualizar_produto_existente(self.produtos_cadastrados, self.indice_selecionado, nome, preco, quantidade)
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            self.cancelar_edicao() # Reseta o modo de edição após salvar

        # A aba informa ao App principal para atualizar sua Listbox
        self.update_listbox_callback()

        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.nome_entry.focus_set()

    def excluir_produto(self):
        selected_indices = self.produtos_listbox.curselection()

        if not selected_indices:
            messagebox.showwarning("Nenhum Item Selecionado", "Por favor, selecione um produto para excluir.")
            return

        index_to_delete = selected_indices[0]
        produto_nome = self.produtos_cadastrados[index_to_delete].nome

        confirm = messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o produto '{produto_nome}'?"
        )

        if confirm:
            excluir_produto_por_indice(self.produtos_cadastrados, index_to_delete)
            messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")

            if self.indice_selecionado is not None and self.indice_selecionado == index_to_delete:
                self.cancelar_edicao()

            self.update_listbox_callback() # A aba informa ao App principal para atualizar

    def carregar_para_edicao(self, event):
        selected_indices = self.produtos_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Nenhum Item Selecionado", "Por favor, selecione um produto para editar.")
            return

        self.indice_selecionado = selected_indices[0]
        produto_selecionado = self.produtos_cadastrados[self.indice_selecionado]

        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, produto_selecionado.nome)

        self.preco_entry.delete(0, tk.END)
        self.preco_entry.insert(0, produto_selecionado.preco)

        self.quantidade_entry.delete(0, tk.END)
        self.quantidade_entry.insert(0, produto_selecionado.quantidade)

        self.cadastrar_button.config(text="Salvar Alterações")
        self.cancelar_button.grid(row=4, column=0, columnspan=2, pady=5)
        self.nome_entry.focus_set()

    def cancelar_edicao(self):
        self.indice_selecionado = None
        self.cadastrar_button.config(text="Cadastrar")
        self.cancelar_button.grid_forget()

        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.nome_entry.focus_set()