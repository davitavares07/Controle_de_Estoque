import tkinter as tk
from tkinter import ttk

class NovaAbaVazia(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # O 'parent' aqui também é o ttk.Notebook

        # Adicione widgets para esta aba aqui
        ttk.Label(self, text="Esta é a nova aba vazia, separada em seu próprio arquivo!").pack(pady=50, padx=50)
        ttk.Label(self, text="Use este espaço para adicionar novas funcionalidades.").pack(pady=10, padx=50)

        # Exemplo de botão
        ttk.Button(self, text="Clique-me!").pack(pady=20)