import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from database import Database

class Produto:
    def __init__(self, interface, controller):
        self.interface = interface
        self.controller = controller
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
                    periodo_id = periodo_aberto[0]  # Extrai o PeriodoID da tupla
                    self.database.inserir_produto(nome, valor, quantidade, data_entrada, hora_entrada, periodo_id)
                    messagebox.showinfo("Produto Cadastrado", "O produto foi cadastrado com sucesso.")
                    self.interface.entry_nome.delete(0, tk.END)
                    self.interface.entry_valor.delete(0, tk.END)
                    self.interface.entry_quantidade.delete(0, tk.END)
                    self.interface.tabela_produtos_cadastrados.delete(*self.interface.tabela_produtos_cadastrados.get_children())  # Limpar lista de produtos
                    self.exibir_produtos()  # Carregar novos dados de produtos
                    self.carrega_produtos_combobox() #carrega as combobox
                    self.interface.vendas.carregar_produtos_combobox_venda()  # Atualizar a ComboBox de produtos na tela de vendas
                else:
                    messagebox.showerror("Erro", "Valor e quantidade devem ser números.")
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")

    def excluir_produto(self):
        selecionado = self.interface.combobox_produtos.get()
        periodo_aberto = self.database.obter_periodo_aberto()  # Obter o período em aberto
        if periodo_aberto:
            periodo_aberto_id = periodo_aberto[0]  # Extrai o PeriodoID da tupla
            produto_id = self.database.obter_id_produto(selecionado, periodo_aberto_id)  # Passar o ID do período em aberto

            if produto_id is not None:
                opcao = messagebox.askquestion("Excluir Produto", "Deseja realmente excluir o produto selecionado?")
                if opcao == 'yes':
                    self.database.excluir_produto(produto_id)
                    messagebox.showinfo("Produto Excluído", "O produto foi excluído com sucesso.")
                    self.interface.entry_nome_edicao.delete(0, tk.END)
                    self.interface.entry_valor_edicao.delete(0, tk.END)
                    self.interface.entry_quantidade_edicao.delete(0, tk.END)
                    self.interface.tabela_produtos_cadastrados.delete(*self.interface.tabela_produtos_cadastrados.get_children())  # Limpar tabela de produtos cadastrados
                    self.interface.label_cadastro_info_data.config(text="")
                    self.interface.label_cadastro_info_hora.config(text="")
                    self.interface.atualizar_tabela_produtos_cadastrados()  # Atualizar a tabela de produtos cadastrados
                    self.carrega_produtos_combobox()  # Carregar novos dados na combobox
                    self.interface.vendas.carregar_produtos_combobox_venda()  # Atualizar a ComboBox de produtos na tela de vendas
                else:
                    messagebox.showinfo("Exclusão Cancelada", "A exclusão do produto foi cancelada.")
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")
        else:
            messagebox.showwarning("Período não Iniciado", "Não há período em aberto. Inicie um período antes de excluir produtos.")

    def carregar_produtos_cadastrados(self):
        produtos_cadastrados = self.database.obter_nomes_produtos()
        self.interface.combobox_produtos['values'] = produtos_cadastrados
        
    def carregar_dados_produto(self, event):
        produto = self.interface.combobox_produtos.get()
        periodo_aberto = self.database.obter_periodo_aberto()  # Obter o período em aberto
        if periodo_aberto:
            periodo_aberto_id = periodo_aberto[0]  # Extrai o PeriodoID da tupla
            produto_id = self.database.obter_id_produto(produto, periodo_aberto_id)  # Passar o ID do período em aberto

            if produto_id is not None:
                dados_produto = self.database.obter_dados_completos_produto(produto_id)

                if dados_produto:
                    nome, valor, quantidade, data_entrada, hora_entrada = dados_produto

                    self.interface.entry_nome_edicao.delete(0, tk.END)
                    self.interface.entry_nome_edicao.insert(tk.END, nome)

                    self.interface.entry_valor_edicao.delete(0, tk.END)
                    self.interface.entry_valor_edicao.insert(tk.END, valor)

                    self.interface.entry_quantidade_edicao.delete(0, tk.END)
                    self.interface.entry_quantidade_edicao.insert(tk.END, quantidade)

                    self.interface.label_cadastro_info_data.config(text=f"Data: {data_entrada}")
                    self.interface.label_cadastro_info_hora.config(text=f"Hora: {hora_entrada}")
                else:
                    messagebox.showerror("Erro", "Falha ao carregar os dados do produto.")
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")
        else:
            messagebox.showwarning("Período não Iniciado", "Não há período em aberto. Inicie um período antes de carregar os dados do produto.")

    def salvar_edicao_produto(self):
        selecionado = self.interface.combobox_produtos.get()
        periodo_aberto = self.controller.obter_periodo_aberto()  # Obter o período em aberto
        if periodo_aberto:
            periodo_aberto_id = periodo_aberto[0]  # Extrai o PeriodoID da tupla
            produto_id = self.database.obter_id_produto(selecionado, periodo_aberto_id)  # Passar o ID do período em aberto

            if produto_id is not None:
                nome = self.interface.entry_nome_edicao.get()
                valor = self.interface.entry_valor_edicao.get()
                quantidade = self.interface.entry_quantidade_edicao.get()

                if nome and valor and quantidade:
                    if self.is_numero(valor) and self.is_numero(quantidade):
                        self.database.atualizar_produto(produto_id, nome, valor, quantidade)
                        messagebox.showinfo("Produto Atualizado", "O produto foi atualizado com sucesso.")
                        self.interface.entry_nome_edicao.delete(0, tk.END)
                        self.interface.entry_valor_edicao.delete(0, tk.END)
                        self.interface.entry_quantidade_edicao.delete(0, tk.END)
                        self.interface.atualizar_tabela_produtos_cadastrados()  # Atualizar a tabela de produtos cadastrados
                        self.interface.vendas.carregar_produtos_combobox_venda()  # Atualizar a ComboBox de produtos na tela de vendas
                        self.carrega_produtos_combobox()
                        
                    else:
                        messagebox.showerror("Erro", "Valor e quantidade devem ser números.")
                else:
                    messagebox.showerror("Erro", "Preencha todos os campos.")
            else:
                messagebox.showerror("Erro", "Produto não encontrado.")
        else:
            messagebox.showwarning("Período não Iniciado", "Não há período em aberto. Inicie um período antes de salvar as alterações do produto.")


            
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
            self.interface.tabela_produtos_cadastrados.delete(*self.interface.tabela_produtos_cadastrados.get_children())
            nomes_produtos = [produto[1] for produto in produtos]

            for produto in produtos:
                nome = produto[1]
                valor = produto[2]
                quantidade = produto[3]
                produto_formatado = f"Nome: {nome}, Valor: {valor}, Quantidade: {quantidade}"
                self.interface.tabela_produtos_cadastrados.insert("", tk.END, values=(nome, f"R$ {valor:.2f}", quantidade))

    def carrega_produtos_combobox(self):
        periodo_aberto = self.database.obter_periodo_aberto()
        if not periodo_aberto:
            messagebox.showwarning("Período não Iniciado", "Não há período em aberto.")
        else:
            periodo_id = periodo_aberto[0]
            produtos = self.database.obter_produtos_periodo(periodo_id)
            nomes_produtos = [produto[1] for produto in produtos]
            self.interface.combobox_produtos['values'] = nomes_produtos

    def is_numero(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
