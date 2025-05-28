import tkinter as tk
from tkinter import ttk
from dados_banco import carregar_produtos # Apenas para carregar a lista inicial
from cadastro_tab import CadastroProdutosTab # Importa a classe da aba de cadastro
from relatorio import NovaAbaVazia # Importa a classe da nova aba

class AppPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Produtos")
        self.geometry("1024x768")

        # A lista de produtos é mantida aqui no AppPrincipal,
        # e passada como referência para as abas que precisam dela.
        self.produtos_cadastrados = carregar_produtos()

        self.create_widgets()

        # Garante que a Listbox da aba de cadastro seja atualizada ao iniciar
        # self.cadastro_tab.atualizar_listbox() # Já é chamado dentro do self.cadastro_tab.__init__
                                              # ou pode ser chamada explicitamente aqui

    def create_widgets(self):
        # --- Configuração do Notebook (Abas) ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)


        # --- Aba 1: Cadastro e Listagem de Produtos ---
        # Instancia a aba de cadastro, passando a lista de produtos
        # e o método de atualização da listbox (da própria aba, que precisa ser acessível)
        self.cadastro_tab = CadastroProdutosTab(
            self.notebook,
            self.produtos_cadastrados,
            self.cadastro_tab_update_listbox_callback # Passa uma função para a aba usar
        )
        self.notebook.add(self.cadastro_tab, text="Cadastro de Produtos")


        # --- Aba 2: Nova Aba em Branco ---
        self.nova_tab = NovaAbaVazia(self.notebook) # Instancia a nova aba vazia
        self.notebook.add(self.nova_tab, text="Nova Aba Vazia")
        self.cadastro_tab.atualizar_listbox()


    def cadastro_tab_update_listbox_callback(self):
        """
        Callback para ser usada pela CadastroProdutosTab para pedir ao AppPrincipal
        que sua Listbox seja atualizada.
        Isso desacopla a lógica de atualização da Listbox da lógica de dados.
        """
        self.cadastro_tab.atualizar_listbox()


# Bloco principal para rodar a aplicação
if __name__ == "__main__":
    app = AppPrincipal()
    app.mainloop()