import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import Database

class Produto:
    def __init__(self, interface):
        self.interface = interface
        self.database = Database()

    def cadastrar_produto(self):
        periodo_aberto = self.database.obter_periodo_aberto()
        if not periodo_aberto:
            messagebox.showwarning("Período não Iniciado", "Não há período em aberto. Inicie um período antes de cadastrar produtos.")
        else:
            nome = self.interface.entry_nome.get()
            valor = self.interface.entry_valor.get()
            quantidade = self.interface.entry_quantidade.get()
            data_entrada = datetime.now().strftime("%d-%m-%Y")
            hora_entrada = datetime.now().strftime("%H:%M:%S")

            if nome and valor and quantidade:
                if self.is_numero(valor) and self.is_numero(quantidade):
                    self.database.inserir_produto(nome, valor, quantidade, data_entrada, hora_entrada)
                    messagebox.showinfo("Produto Cadastrado", "O produto foi cadastrado com sucesso.")
                    self.interface.entry_nome.delete(0, tk.END)
                    self.interface.entry_valor.delete(0, tk.END)
                    self.interface.entry_quantidade.delete(0, tk.END)
                    self.interface.lista_produtos.delete(0, tk.END)  # Limpar lista de produtos
                    self.exibir_produtos()  # Carregar novos dados de produtos
                else:
                    messagebox.showerror("Erro", "Valor e quantidade devem ser números.")
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")

    def editar_produto(self):
        selecionado = self.interface.lista_produtos.curselection()
        if selecionado:
            produto = self.interface.lista_produtos.get(selecionado[0])
            nome, valor, quantidade = self.obter_dados_produto(produto)

            self.interface.entry_nome.delete(0, tk.END)
            self.interface.entry_nome.insert(tk.END, nome)

            self.interface.entry_valor.delete(0, tk.END)
            self.interface.entry_valor.insert(tk.END, valor)

            self.interface.entry_quantidade.delete(0, tk.END)
            self.interface.entry_quantidade.insert(tk.END, quantidade)
        else:
            messagebox.showerror("Erro", "Selecione um produto para editar.")

    def obter_dados_produto(self, produto):
        dados = produto.split(", ")
        nome = dados[0].split(": ")[1]
        valor = dados[1].split(": ")[1]
        quantidade = dados[2].split(": ")[1]
        return nome, valor, quantidade

    def exibir_produtos(self):
        periodo_aberto = self.database.obter_periodo_aberto()
        if not periodo_aberto:
            messagebox.showwarning("Período não Iniciado", "Não há período em aberto.")
        else:
            periodo_id = periodo_aberto[0]
            produtos = self.database.obter_produtos_periodo(periodo_id)
            self.interface.lista_produtos.delete(0, tk.END)

            for produto in produtos:
                nome = produto[1]
                valor = produto[2]
                quantidade = produto[3]
                produto_formatado = f"Nome: {nome}, Valor: {valor}, Quantidade: {quantidade}"
                self.interface.lista_produtos.insert(tk.END, produto_formatado)

    def is_numero(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
