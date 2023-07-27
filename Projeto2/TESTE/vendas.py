from datetime import datetime
from tkinter import messagebox
from database import Database
import tkinter as tk

class Vendas:
    def __init__(self, interface, controller):
        self.interface = interface
        self.controller = controller
        self.database = controller.database
        self.interface = controller.interface
        self.produtos_selecionados = []  # Lista para armazenar os produtos selecionados na venda

    def registrar_venda(self, produto, quantidade, valor_total, venda_cortesia):
        # Lógica de negócios para registrar a venda

        # Obter o ID do período aberto
        periodo_aberto = self.controller.obter_id_periodo_aberto()
        if not periodo_aberto:
            # Não há período aberto para registrar a venda
            return False

        periodo_id = periodo_aberto[0]

        # Obter o ID do produto
        produto_id = self.controller.obter_id_produto_por_nome(produto, periodo_id)
        if not produto_id:
            # Produto não encontrado
            return False

        # Registrar a venda no banco de dados
        data_hora_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.controller.registrar_venda(data_hora_atual, produto, quantidade, valor_total, periodo_id, venda_cortesia, produto_id)

        return True
    
    def excluir_produto_venda(self):
        selecionado = self.interface.lista_produtos_venda.curselection()

        if selecionado:
            index = selecionado[0]
            self.interface.lista_produtos_venda.delete(index)
            del self.produtos_selecionados[index]
        else:
            messagebox.showwarning("Selecione um produto", "Selecione um produto na lista para excluir.")

    def exibir_itens_venda(self):
        self.interface.lista_produtos_venda.delete(0, tk.END)  # Limpa a listbox

        for produto in self.produtos_selecionados:
            # Formatando a quantidade como inteiro
            quantidade_formatada = int(produto['quantidade'])
            item_formatado = f"QTD: {quantidade_formatada} | CORTESIA: {'Sim' if produto['cortesia'] else 'Não'} | ITEM: {produto['nome']}"
            self.interface.lista_produtos_venda.insert(tk.END, item_formatado)

    def adicionar_produto_venda(self):
        produto_selecionado = self.interface.combobox_produtos_venda.get()
        quantidade_selecionada = self.interface.entry_quantidade_venda.get()

        # Verifica se a quantidade é um número válido inteiro
        if self.is_int(quantidade_selecionada):
            quantidade_selecionada = int(quantidade_selecionada)  # Converter para inteiro
            if quantidade_selecionada > 0:
                venda_cortesia = self.interface.venda_cortesia_var.get()  # Verifica se é uma venda cortesia

                produto = {
                    "nome": produto_selecionado,
                    "quantidade": quantidade_selecionada,
                    "cortesia": venda_cortesia  # Inclui a informação se a venda é uma cortesia ou não
                }

                self.produtos_selecionados.append(produto)
                self.interface.label_quantidade_venda.config(text="")
                self.interface.combobox_produtos_venda.set("")
                self.interface.entry_quantidade_venda.delete(0, tk.END)
                self.exibir_itens_venda()  # Atualiza a exibição na lista de vendas
            else:
                messagebox.showwarning("Quantidade Inválida", "A quantidade deve ser maior que zero.")
        else:
            messagebox.showwarning("Quantidade Inválida", "Digite uma quantidade válida (número inteiro).")

    def carregar_produtos_combobox_venda(self):
        self.interface.combobox_produtos_venda['values'] = []
        self.interface.lista_produtos_venda.delete(0, tk.END)  # Limpar a lista de produtos selecionados
        periodo_aberto = self.controller.obter_periodo_aberto()
        if periodo_aberto:
            periodo_id = periodo_aberto[0]
            produtos_dados_completos = self.database.obter_produtos_periodo(periodo_id)
            if produtos_dados_completos is not None:
                produtos_nomes = [produto[1] for produto in produtos_dados_completos]
                self.interface.combobox_produtos_venda['values'] = produtos_nomes
                self.interface.combobox_produtos_venda.current(0)
            else:
                messagebox.showwarning("Produtos não encontrados", "Não há produtos cadastrados para o período em aberto.")
        else:
            messagebox.showwarning("Período não encontrado", "Não há período de vendas aberto.")

    def atualizar_quantidade_disponivel(self, event=None):
        produto_selecionado = self.interface.combobox_produtos_venda.get()
        if produto_selecionado:
            periodo_aberto = self.controller.obter_id_periodo_aberto()
            if periodo_aberto:
                periodo_id = periodo_aberto[0]
                produto_id = self.controller.obter_id_produto_por_nome(produto_selecionado, periodo_id)
                if produto_id is not None:
                    quantidade_disponivel = self.controller.obter_quantidade_produto(produto_id)
                    self.interface.label_quantidade_venda.config(text=f"Quantidade disponível: {quantidade_disponivel}")
                else:
                    self.interface.label_quantidade_venda.config(text="")
            else:
                self.interface.label_quantidade_venda.config(text="")
        else:
            self.interface.label_quantidade_venda.config(text="")
        

    def obter_valor_produto(self, produto):
        periodo_aberto = self.controller.obter_id_periodo_aberto()
        if periodo_aberto:
            periodo_id = periodo_aberto[0]
            return self.controller.obter_valor_produto(produto, periodo_id)
        return None
    
    def is_numero(self, valor):
        try:
            float(valor)
            return True
        except ValueError:
            return False
        
    def is_int(self, valor):
        try:
            int(valor)
            return True
        except ValueError:
            return False    

        
