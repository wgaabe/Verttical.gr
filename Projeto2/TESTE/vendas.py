from datetime import datetime
from tkinter import messagebox
from database import Database
import tkinter as tk
from tkinter import ttk

class Vendas:
    def __init__(self, interface, controller):
        self.interface = interface
        self.controller = controller
        self.database = controller.database
        self.interface = controller.interface
        self.produtos_selecionados = []  # Lista para armazenar os produtos selecionados na venda
        self.valor_total_venda = 0.0  # Variável para armazenar o valor total da venda
        self.lista_produtos_venda = []  # Lista para armazenar os produtos da venda
        self.tabela_vendas_selecionada = None  # Variável para armazenar a venda selecionada na tabela

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
        selecionado = self.interface.tabela_vendas.selection()
        if selecionado:
            venda_selecionada = self.interface.tabela_vendas.item(selecionado[0])
            produto_nome = venda_selecionada["values"][0]
            produto_selecionado = None

            # Procura o produto selecionado na lista de produtos
            for produto in self.produtos_selecionados:
                if produto["nome"] == produto_nome:
                    produto_selecionado = produto
                    break

            if produto_selecionado:
                # Confirmação antes de excluir o produto da venda
                resposta = messagebox.askyesno("Excluir Produto",
                                            f"Deseja excluir o produto '{produto_nome}' da venda?")
                if resposta:
                    self.produtos_selecionados.remove(produto_selecionado)
                    self.exibir_itens_venda()
                    self.atualizar_total_venda()
                else:
                    messagebox.showinfo("Exclusão Cancelada", "A exclusão do produto foi cancelada.")
            else:
                messagebox.showwarning("Produto não encontrado",
                                    "O produto selecionado não foi encontrado na lista de produtos da venda.")
        else:
            messagebox.showwarning("Nenhum Produto Selecionado", "Selecione um produto na lista para excluir.")


    def atualizar_total_venda(self):
        total_venda = 0
        for produto in self.produtos_selecionados:
            if not produto["cortesia"]:
                total_venda += produto["valor_total_produto"]
        self.interface.label_total_venda.config(text=f"Total da Venda: R$ {total_venda:.2f}")

    def exibir_itens_venda(self):
        # Limpar a tabela antes de exibir os itens
        self.limpar_tabela_vendas()

        # Exibir os produtos da venda na tabela
        for produto in self.produtos_selecionados:
            self.interface.tabela_vendas.insert("", tk.END, values=(produto["nome"], produto["quantidade"], "Sim" if produto["cortesia"] else "Não", produto["valor_unitario"], produto["valor_total_produto"]))

        # Atualiza o valor total da venda após exibir os itens
        self.atualizar_total_venda()


    def adicionar_produto_venda(self,produto_selecionado, quantidade_selecionada, venda_cortesia):
        produto_selecionado = self.interface.combobox_produtos_venda.get()
        quantidade_selecionada = self.interface.entry_quantidade_venda.get()

        # Verifica se a quantidade é um número válido
        if self.is_numero(quantidade_selecionada):
            quantidade_selecionada = float(quantidade_selecionada)
            if quantidade_selecionada > 0:
                # Corrigir a chamada da função obter_dados_produto_por_periodo para incluir o período_id correto
                periodo_id = self.controller.obter_id_periodo_aberto()[0]  # Obter o ID do período aberto
                dados_produto = self.controller.obter_dados_produto_por_periodo(produto_selecionado, periodo_id)

                if dados_produto:
                    nome_produto, valor_produto, quantidade_produto, _, _ = dados_produto
                    valor_total_produto = valor_produto * quantidade_selecionada

                    produto = {
                        "nome": produto_selecionado,
                        "quantidade": quantidade_selecionada,
                        "cortesia": self.interface.venda_cortesia_var.get(),  # Verifica se é uma venda cortesia
                        "valor_unitario": valor_produto,
                        "valor_total_produto": valor_total_produto
                    }

                    self.produtos_selecionados.append(produto)
                    self.interface.label_quantidade_venda.config(text="")
                    self.interface.combobox_produtos_venda.set("")
                    self.interface.venda_cortesia_var.set(False)  # Desmarca a caixa de seleção "Venda Cortesia"
                    self.interface.entry_quantidade_venda.delete(0, tk.END)
                    self.exibir_itens_venda()  # Atualiza a exibição na lista de vendas
                    self.atualizar_total_venda()  # Atualiza o total geral da venda
                else:
                    messagebox.showwarning("Produto não encontrado", "O produto selecionado não foi encontrado para o período em aberto.")
            else:
                messagebox.showwarning("Quantidade Inválida", "A quantidade deve ser maior que zero.")
        else:
            messagebox.showwarning("Quantidade Inválida", "Digite uma quantidade válida (número).")

    def carregar_produtos_combobox_venda(self):
        self.interface.combobox_produtos_venda['values'] = []
        #self.interface.lista_produtos_venda_tabela.delete(0, tk.END)  # Limpar a lista de produtos selecionados
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

    def limpar_tabela_vendas(self):
        for item in self.interface.tabela_vendas.get_children():
            self.interface.tabela_vendas.delete(item)

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
    
    def limpar_toda_lista_vendas(self):
        if messagebox.askokcancel("Limpar Lista de Vendas", "Deseja realmente limpar a lista de vendas?"):
            # Limpar a lista de produtos selecionados
            self.produtos_selecionados = []

            # Limpar a exibição dos itens na lista de vendas na interface
            self.limpar_tabela_vendas()

            # Zerar o valor total da venda na interface
            self.interface.label_total_venda.config(text="Total da Venda: R$ 0.00")

            # Desmarcar a opção de venda cortesia na interface
            self.interface.venda_cortesia_var.set(False)
    
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

        
