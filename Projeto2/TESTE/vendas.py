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
        self.produtos_cortesia_selecionados = []  # Lista para armazenar os produtos de cortesia selecionados na venda
        self.valor_total_venda = 0.0  # Variável para armazenar o valor total da venda
        self.lista_produtos_venda = []  # Lista para armazenar os produtos da venda
        self.tabela_vendas_selecionada = None  # Variável para armazenar a venda selecionada na tabela
        self.interface = interface

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
            for item in selecionado:
                venda_selecionada = self.interface.tabela_vendas.item(item)
                produto_nome = venda_selecionada["values"][0]
                produto_quantidade = venda_selecionada["values"][1]
                is_cortesia = "Sim" in venda_selecionada["values"][2]

                mensagem_cortesia = "cortesia" if is_cortesia else "normal"

                resposta = messagebox.askyesno("Excluir Produto",
                                                f"Deseja excluir a venda {mensagem_cortesia} do produto '{produto_nome}' com quantidade {produto_quantidade}?")
                if resposta:
                    produto_selecionado = None

                    # Procura o produto selecionado na lista de produtos cortesia
                    if is_cortesia:
                        for produto_cortesia in self.produtos_cortesia_selecionados:
                            if produto_cortesia["nome"] == produto_nome:
                                produto_selecionado = produto_cortesia
                                break
                    # Se não for uma venda cortesia, procura na lista de produtos normais
                    else:
                        for produto in self.produtos_selecionados:
                            if produto["nome"] == produto_nome:
                                produto_selecionado = produto
                                break

                    if produto_selecionado:
                        if is_cortesia:
                            # Se for uma venda cortesia, remove o produto da lista de cortesias
                            if produto_selecionado in self.produtos_cortesia_selecionados:
                                self.produtos_cortesia_selecionados.remove(produto_selecionado)
                        else:
                            # Se for uma venda normal, remove o produto da lista de produtos selecionados
                            if produto_selecionado in self.produtos_selecionados:
                                self.produtos_selecionados.remove(produto_selecionado)

                        self.exibir_itens_venda()
                        self.atualizar_total_venda()
                    else:
                        messagebox.showwarning("Produto não encontrado",
                                            "O produto selecionado não foi encontrado na lista de produtos da venda.")
        else:
            messagebox.showwarning("Nenhum Produto Selecionado", "Selecione um produto na lista para excluir.")


    def atualizar_total_venda(self):
        total_venda = 0

        # Somar os valores dos produtos normais na venda
        for produto in self.produtos_selecionados:
            total_venda += produto["valor_total_produto"]

        # Atualizar o valor total da venda na interface
        self.interface.label_total_venda.config(text=f"Total da Venda: R$ {total_venda:.2f}")
       

    def formatar_cortesia(self, value):
        if value:
            return "Sim"
        return "Não"

    def configurar_estilos(self):
        style = ttk.Style()
        style.configure("Cortesia.TLabel", foreground="red")

    def exibir_itens_venda(self):
        # Limpar a tabela antes de exibir os itens
        self.limpar_tabela_vendas()

        # Exibir os produtos da venda na tabela
        for produto in self.produtos_selecionados:
            cortesia = "Sim" if produto["cortesia"] else "Não"
            quantidade_formatada = int(produto["quantidade"])  # Converte para int para remover os decimais
            if produto["cortesia"]:
                self.interface.tabela_vendas.insert("", tk.END, values=(produto["nome"], quantidade_formatada, cortesia, produto["valor_unitario"], produto["valor_total_produto"]), tags=("cortesia",))
            else:
                self.interface.tabela_vendas.insert("", tk.END, values=(produto["nome"], quantidade_formatada, cortesia, produto["valor_unitario"], produto["valor_total_produto"]))

        # Exibir os produtos de cortesia na tabela
        for produto_cortesia in self.produtos_cortesia_selecionados:
            cortesia_cortesia = "Sim"
            quantidade_formatada_cortesia = int(produto_cortesia["quantidade"])  # Converte para int para remover os decimais
            self.interface.tabela_vendas.insert("", tk.END, values=(produto_cortesia["nome"], quantidade_formatada_cortesia, cortesia_cortesia, produto_cortesia["valor_unitario"], produto_cortesia["valor_total_produto"]), tags=("cortesia",))

        # Aplicar o estilo "Cortesia.TLabel" nas linhas que possuem cortesia
        self.interface.tabela_vendas.tag_configure("cortesia", foreground="red")

        # Atualiza o valor total da venda após exibir os itens
        self.atualizar_total_venda()


    def adicionar_produto_venda(self, produto_selecionado, quantidade_selecionada, venda_cortesia):
        # Verifica se a quantidade é um número válido
        if self.is_numero(quantidade_selecionada):
            quantidade_selecionada = float(quantidade_selecionada)
            if quantidade_selecionada > 0:
                periodo_aberto = self.controller.obter_id_periodo_aberto()
                if periodo_aberto:
                    periodo_id = periodo_aberto[0]  # Extrai o PeriodoID da tupla
                    produto_id = self.controller.obter_id_produto(produto_selecionado, periodo_id)
                    if produto_id is not None:
                        estoque_disponivel = self.controller.obter_estoque_disponivel(produto_id, periodo_id)
                        quantidade_na_lista = 0
                        quantidade_cortesia = 0

                        # Verifica a quantidade total de vendas e vendas de cortesia do produto
                        for produto in self.produtos_selecionados:
                            if produto["ID"] == produto_id:
                                quantidade_na_lista += produto["quantidade"]

                        for produto_cortesia in self.produtos_cortesia_selecionados:
                            if produto_cortesia["ID"] == produto_id:
                                quantidade_cortesia += produto_cortesia["quantidade"]

                        quantidade_total = quantidade_na_lista + quantidade_cortesia + quantidade_selecionada
                        quantidade_total_venda = quantidade_na_lista + quantidade_cortesia + quantidade_selecionada

                        if quantidade_total > estoque_disponivel:
                            quantidade_excedente = quantidade_total - estoque_disponivel
                            quantidade_disponivel_para_venda = estoque_disponivel - quantidade_na_lista - quantidade_cortesia

                            mensagem = (
                                f"Quantidade informada pelo usuário: {int(quantidade_selecionada)}\n\n"
                                f"A quantidade total({int(quantidade_total)}) excede o estoque disponível "
                                f"para o produto selecionado ({estoque_disponivel})\n\n"
                                f"Quantidade disponível para venda: {int(quantidade_disponivel_para_venda)}\n\n"
                                f"Quantidade excedente: {int(quantidade_excedente)}\n\n"
                                f"Quantidade em estoque: {int(estoque_disponivel)}\n"
                                f"Quantidade já vendida: {int(quantidade_na_lista)}\n"
                                f"Quantidade de cortesia vendida: {int(quantidade_cortesia)}"
                            )
                            messagebox.showwarning("Quantidade Inválida", mensagem)
                            return

                        dados_produto = self.controller.obter_dados_produto_por_periodo(produto_selecionado, periodo_id)
                        if dados_produto:
                            nome_produto, valor_produto, _, _, _ = dados_produto
                            valor_total_produto = valor_produto * quantidade_selecionada

                            produto = {
                                "ID": produto_id,
                                "nome": produto_selecionado,
                                "quantidade": quantidade_selecionada,
                                "cortesia": venda_cortesia,
                                "valor_unitario": valor_produto,
                                "valor_total_produto": valor_total_produto
                            }

                            if venda_cortesia:
                                self.produtos_cortesia_selecionados.append(produto)
                            else:
                                self.produtos_selecionados.append(produto)

                            self.interface.label_quantidade_venda.config(text="")
                            self.interface.combobox_produtos_venda.set("")
                            self.interface.venda_cortesia_var.set(False)
                            self.interface.entry_quantidade_venda.delete(0, tk.END)
                            self.exibir_itens_venda()
                            self.atualizar_total_venda()
                        else:
                            messagebox.showwarning("Produto não encontrado", "O produto selecionado não foi encontrado para o período em aberto.")
                    else:
                        messagebox.showwarning("Produto não encontrado", "O produto selecionado não foi encontrado para o período em aberto.")
                else:
                    messagebox.showwarning("Período não Iniciado", "Não há período em aberto. Inicie um período antes de adicionar produtos à venda.")
            else:
                messagebox.showwarning("Quantidade Inválida", "A quantidade deve ser maior que zero.")
        else:
            messagebox.showwarning("Quantidade Inválida", "Digite uma quantidade válida (número).")






    # Resto do código da classe Vendas

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
                if len(produtos_nomes) > 0:  # Verifica se a lista tem itens antes de definir o índice atual
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
            # Limpar as listas de produtos selecionados e produtos de cortesia selecionados
            self.produtos_selecionados = []
            self.produtos_cortesia_selecionados = []
            # Limpar a exibição dos itens na tabela de vendas na interface
            self.exibir_itens_venda()
            # Zerar o valor total da venda na interface
            self.interface.label_total_venda.config(text="Total da Venda: R$ 0.00")
            # Desmarcar a opção de venda cortesia na interface
            self.interface.venda_cortesia_var.set(False)
            # Limpar a ComboBox de produtos
            self.interface.combobox_produtos_venda.set("")
            # Limpar o campo de quantidade
            self.interface.entry_quantidade_venda.delete(0, tk.END)
            # Limpar a label de quantidade disponível
            self.interface.label_quantidade_venda.config(text="")

    def limpar_itens_venda(self):
        self.limpar_tabela_vendas()    

    def limpar_campos_vendas_finalizar_periodo(self):
        # Limpar a lista de produtos selecionados
        self.produtos_selecionados = []
        # Limpar a exibição dos itens na lista de vendas na interface
        self.limpar_tabela_vendas()  # Atualize aqui o nome da função corretamente
        # Zerar o valor total da venda na interface
        self.interface.label_total_venda.config(text="Total da Venda: R$ 0.00")
        # Desmarcar a opção de venda cortesia na interface
        self.interface.venda_cortesia_var.set(False)
        # Limpar a ComboBox de produtos
        self.interface.combobox_produtos_venda.set("")
        # Limpar o campo de quantidade
        self.interface.entry_quantidade_venda.delete(0, tk.END)
        # Limpar a label de quantidade disponível
        self.interface.label_quantidade_venda.config(text="")
      
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

        
