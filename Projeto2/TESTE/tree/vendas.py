from datetime import datetime
from tkinter import messagebox
from database import Database
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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
        self.janela_qrcode = None  # Variável para armazenar a janela do QR Code do PIX

    def limpar_vendas_selecionadas(self):
        self.produtos_selecionados = []
        self.produtos_cortesia_selecionados = []

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
                            if produto_cortesia["nome"] == produto_selecionado:
                                quantidade_cortesia += produto_cortesia["quantidade"]

                        quantidade_total = quantidade_na_lista + quantidade_cortesia + quantidade_selecionada

                        if quantidade_total > estoque_disponivel:
                            quantidade_excedente = quantidade_total - estoque_disponivel
                            quantidade_disponivel_para_venda = estoque_disponivel - quantidade_na_lista - quantidade_cortesia

                            mensagem = (
                                f"Produto selecionado: {produto_selecionado}\n"
                                f"Quantidade informada pelo usuário: {int(quantidade_selecionada)}\n\n"
                                f"A quantidade total({int(quantidade_total)}) excede o estoque disponível "
                                f"para o produto selecionado ({estoque_disponivel})\n\n"
                                f"Quantidade excedente: {int(quantidade_excedente)}\n\n"
                                f"Quantidade em estoque: {int(estoque_disponivel)}\n\n"
                                f"------------------Em Venda-----------------\n"
                                f"Quantidade já vendida: {int(quantidade_na_lista)}\n"
                                f"Quantidade de cortesia vendida: {int(quantidade_cortesia)}\n"
                                f"-----------------------------------------------\n\n"
                                f"++++++++++++++++++++++++++\n"
                                f"Quantidade disponível para venda: {int(quantidade_disponivel_para_venda)}\n"
                                f"++++++++++++++++++++++++++\n\n"
                            )
                            messagebox.showwarning("Quantidade Inválida", mensagem)
                            return

                        dados_produto = self.controller.obter_dados_produto_por_periodo(produto_selecionado, periodo_id)
                        if dados_produto:
                            nome_produto, valor_produto, _, _, _ = dados_produto
                            valor_total_produto = valor_produto * quantidade_selecionada

                            if venda_cortesia:
                                produto_cortesia_existente = None
                                for produto_cortesia in self.produtos_cortesia_selecionados:
                                    if produto_cortesia["ID"] == produto_id:
                                        produto_cortesia_existente = produto_cortesia
                                        break

                                if produto_cortesia_existente:
                                    produto_cortesia_existente["quantidade"] += quantidade_selecionada
                                    produto_cortesia_existente["valor_total_produto"] = produto_cortesia_existente["valor_unitario"] * produto_cortesia_existente["quantidade"]
                                else:
                                    novo_produto_cortesia = {
                                        "ID": produto_id,
                                        "nome": produto_selecionado,
                                        "quantidade": quantidade_selecionada,
                                        "valor_unitario": valor_produto,
                                        "valor_total_produto": valor_total_produto
                                    }
                                    self.produtos_cortesia_selecionados.append(novo_produto_cortesia)
                            else:
                                produto_existente = None
                                for produto in self.produtos_selecionados:
                                    if produto["ID"] == produto_id:
                                        produto_existente = produto
                                        break

                                if produto_existente:
                                    produto_existente["quantidade"] += quantidade_selecionada
                                    produto_existente["valor_total_produto"] = produto_existente["valor_unitario"] * produto_existente["quantidade"]
                                else:
                                    novo_produto = {
                                        "ID": produto_id,
                                        "nome": produto_selecionado,
                                        "quantidade": quantidade_selecionada,
                                        "cortesia": venda_cortesia,
                                        "valor_unitario": valor_produto,
                                        "valor_total_produto": valor_total_produto
                                    }
                                    self.produtos_selecionados.append(novo_produto)

                            # Limpa os campos após adicionar o produto
                            self.interface.label_quantidade_venda.config(text="")
                            self.interface.combobox_produtos_venda.set("")
                            self.interface.venda_cortesia_var.set(False)
                            self.interface.entry_quantidade_venda.delete(0, tk.END)

                            # Atualiza a exibição na tabela
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

    def exibir_itens_venda(self):
        # Limpar a tabela antes de exibir os itens
        self.limpar_tabela_vendas()

        # Exibir os produtos da venda na tabela
        for produto in self.produtos_selecionados:
            cortesia = "Sim" if produto["cortesia"] else "Não"
            quantidade_formatada = int(produto["quantidade"])  # Converte para int para remover os decimais
            item_id = self.interface.tabela_vendas.insert("", tk.END, values=(produto["nome"], quantidade_formatada, cortesia, produto["valor_unitario"], produto["valor_total_produto"]))
            if produto["cortesia"]:
                self.interface.tabela_vendas.item(item_id, tags=("cortesia",))
        # Exibir os produtos de cortesia na tabela
        for produto_cortesia in self.produtos_cortesia_selecionados:
            cortesia_cortesia = "Sim"
            quantidade_formatada_cortesia = int(produto_cortesia["quantidade"])  # Converte para int para remover os decimais
            item_id = self.interface.tabela_vendas.insert("", tk.END, values=(produto_cortesia["nome"], quantidade_formatada_cortesia, cortesia_cortesia, produto_cortesia["valor_unitario"], produto_cortesia["valor_total_produto"]))
            self.interface.tabela_vendas.item(item_id, tags=("cortesia",))

        # Aplicar o estilo "Cortesia.TLabel" nas linhas que possuem cortesia
        self.interface.tabela_vendas.tag_configure("cortesia", foreground="red")

        # Atualiza o valor total da venda após exibir os itens
        self.atualizar_total_venda()

    def atualizar_tabela_vendas(self):
        # Limpar a tabela antes de exibir os itens
        self.limpar_tabela_vendas()

        # Exibir os produtos da venda na tabela
        for produto in self.produtos_selecionados:
            cortesia = "Sim" if produto["cortesia"] else "Não"
            quantidade_formatada = int(produto["quantidade"])  # Converte para int para remover os decimais
            item_id = self.interface.tabela_vendas.insert("", tk.END, values=(produto["nome"], quantidade_formatada, cortesia, produto["valor_unitario"], produto["valor_total_produto"]))
            if produto["cortesia"]:
                self.interface.tabela_vendas.item(item_id, tags=("cortesia",))

        # Exibir os produtos de cortesia na tabela de vendas
        for produto_cortesia in self.produtos_cortesia_selecionados:
            cortesia_cortesia = "Sim"
            quantidade_formatada_cortesia = int(produto_cortesia["quantidade"])  # Converte para int para remover os decimais
            item_id = self.interface.tabela_vendas.insert("", tk.END, values=(produto_cortesia["nome"], quantidade_formatada_cortesia, cortesia_cortesia, produto_cortesia["valor_unitario"], produto_cortesia["valor_total_produto"]))
            self.interface.tabela_vendas.item(item_id, tags=("cortesia",))

        # Aplicar o estilo "Cortesia.TLabel" nas linhas que possuem cortesia
        self.interface.tabela_vendas.tag_configure("cortesia", foreground="red")

        # Atualiza o valor total da venda após exibir os itens
        self.atualizar_total_venda()

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

    def registrar_venda(self):
        # Verificar se existem produtos selecionados para a venda
        if not self.produtos_selecionados and not self.produtos_cortesia_selecionados:
            messagebox.showwarning("Venda Inválida", "Não há produtos selecionados para a venda.")
            return

        # Criar a janela de seleção de método de pagamento
        self.exibir_selecao_metodo_pagamento()

    def exibir_selecao_metodo_pagamento(self):
        janela_metodo_pagamento = tk.Toplevel()
        janela_metodo_pagamento.title("Seleção de Método de Pagamento")

        # Calcula o tamanho da tela e posiciona no centro
        largura_tela = janela_metodo_pagamento.winfo_screenwidth()
        altura_tela = janela_metodo_pagamento.winfo_screenheight()
        largura_janela = 300  # Largura da janela
        altura_janela = 200   # Altura da janela
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        janela_metodo_pagamento.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Funções de callback para os botões de método de pagamento
        def selecionar_dinheiro():
            self.metodo_pagamento = "Dinheiro"
            janela_metodo_pagamento.destroy()
            self.exibir_resumo_venda()

        def selecionar_pix():
            self.metodo_pagamento = "PIX"
            janela_metodo_pagamento.destroy()
            self.exibir_resumo_venda()

        def selecionar_debito():
            self.metodo_pagamento = "Débito"
            janela_metodo_pagamento.destroy()
            self.exibir_resumo_venda()

        def selecionar_credito():
            self.metodo_pagamento = "Crédito"
            janela_metodo_pagamento.destroy()
            self.exibir_resumo_venda()

        # Botões para seleção de método de pagamento
        btn_dinheiro = tk.Button(janela_metodo_pagamento, text="Dinheiro", command=selecionar_dinheiro, width=15)
        btn_dinheiro.pack(pady=10)

        btn_pix = tk.Button(janela_metodo_pagamento, text="PIX", command=selecionar_pix, width=15)
        btn_pix.pack(pady=10)

        btn_debito = tk.Button(janela_metodo_pagamento, text="Débito", command=selecionar_debito, width=15)
        btn_debito.pack(pady=10)

        btn_credito = tk.Button(janela_metodo_pagamento, text="Crédito", command=selecionar_credito, width=15)
        btn_credito.pack(pady=10)

    def exibir_resumo_venda(self):
        
        def selecionar_alterar_pagamento():
            self.janela_resumo.destroy()  # Fecha a janela de resumo da venda
            if self.metodo_pagamento == "PIX" and self.janela_qrcode:
                self.janela_qrcode.destroy()  # Fecha a janela do QR Code do PIX
                self.janela_qrcode = None  # Define a janela do QR Code como None novamente
            self.exibir_selecao_metodo_pagamento()  # Abre uma nova janela de seleção de método de pagamento               
        
        def voltar_tela_vendas():
            self.janela_resumo.destroy()  # Fecha a janela de resumo da venda
            if self.metodo_pagamento == "PIX":
                self.fechar_janela_qrcode()  # Fecha a janela do QR Code do PIX
            #self.exibir_selecao_metodo_pagamento()  # Abre uma nova janela de seleção de método de pagamento
       
        self.janela_resumo = tk.Toplevel()
        self.janela_resumo.title("Resumo da Venda")

        # Calcula o tamanho da tela e posiciona no centro
        largura_tela = self.janela_resumo.winfo_screenwidth()
        altura_tela = self.janela_resumo.winfo_screenheight()
        largura_janela = 500  # Largura da janela
        altura_janela = 400   # Altura da janela
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        self.janela_resumo.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

        # Criar uma Treeview para exibir os produtos
        treeview_produtos = ttk.Treeview(self.janela_resumo, columns=("Produto", "Quantidade", "Valor Unitário"), show="headings")
        treeview_produtos.heading("Produto", text="Produto", anchor=tk.CENTER)  # Centraliza o cabeçalho
        treeview_produtos.heading("Quantidade", text="Quantidade", anchor=tk.CENTER)  # Centraliza o cabeçalho
        treeview_produtos.heading("Valor Unitário", text="Valor Unitário", anchor=tk.CENTER)  # Centraliza o cabeçalho
        
        # Define a altura da treeview com base no número fixo de linhas
        altura_treeview = 8
        treeview_produtos.configure(height=altura_treeview)

        # Define a largura das colunas (ajuste conforme necessário)
        largura_colunas = [100, 100, 150]
        for coluna, largura in zip(("Produto", "Quantidade", "Valor Unitário"), largura_colunas):
            treeview_produtos.column(coluna, width=largura, anchor=tk.CENTER)

        treeview_produtos.pack(padx=20, pady=10)  # Ajusta o padding

        # Preencher a Treeview com os produtos
        for produto in self.produtos_selecionados:
            treeview_produtos.insert("", "end", values=(produto["nome"], int(produto["quantidade"]), f"R$ {produto['valor_unitario']:.2f}"))

        for produto_cortesia in self.produtos_cortesia_selecionados:
            treeview_produtos.insert("", "end", values=(produto_cortesia["nome"], int(produto_cortesia["quantidade"]), "Cortesia"))

        # Configurar tamanho padrão para os botões
        btn_width = 30

        # Calcular o valor total da venda
        valor_total_venda = sum(produto["valor_total_produto"] for produto in self.produtos_selecionados)

        # Botão "Alterar Forma de Pagamento"
        btn_alterar_pagamento = tk.Button(self.janela_resumo, text="Alterar Forma de Pagamento",width=btn_width, command=selecionar_alterar_pagamento)
        btn_alterar_pagamento.pack(padx=20, pady=(10, 0))  # Define o padding somente no topo

        # Botão "Voltar à Tela de Vendas"
        btn_voltar_vendas = tk.Button(self.janela_resumo, text="Voltar à Tela de Vendas",width=btn_width, command=voltar_tela_vendas)
        btn_voltar_vendas.pack(padx=20, pady=5)

        # Label com o método de pagamento
        label_metodo_pagamento = tk.Label(self.janela_resumo, text=f"Método de Pagamento: {self.metodo_pagamento}")
        label_metodo_pagamento.pack(padx=20, pady=5)
      
        # Label com o total da venda (com fonte maior)
        label_total = tk.Label(self.janela_resumo, text=f"Total: R$ {valor_total_venda:.2f}", font=("Helvetica", 14, "bold"))
        label_total.pack(padx=20, pady=(0, 10))  # Define o padding somente na parte inferior

        # Botão para finalizar a venda
        btn_finalizar_venda = tk.Button(self.janela_resumo, text="Finalizar Venda", width=btn_width, command=self.finalizar_venda)
        btn_finalizar_venda.pack(pady=5)

        if self.metodo_pagamento == "PIX":
            self.exibir_qrcode_pix()

    def exibir_qrcode_pix(self):
        if self.metodo_pagamento == "PIX":
            
            # Criação da janela do QR Code aqui
            self.janela_qrcode = tk.Toplevel()
            self.janela_qrcode.title("QR Code PIX")

            qrcode_image = Image.open("img/pix_qrcode.png")  # Caminho correto para a imagem
            qrcode_photo = ImageTk.PhotoImage(qrcode_image)

            # Calcula a posição para centralizar a janela à direita da tela
            largura_tela = self.janela_qrcode.winfo_screenwidth()
            altura_tela = self.janela_qrcode.winfo_screenheight()
            largura_janela = 350
            altura_janela = 350
            padding = 100  # Espaço de padding
            pos_x = largura_tela - largura_janela - padding
            pos_y = (altura_tela - altura_janela) // 2
            self.janela_qrcode.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")

            label_qrcode = tk.Label(self.janela_qrcode, image=qrcode_photo)
            label_qrcode.pack(padx=20, pady=10)

            # Manter a janela aberta até que o usuário a feche
            self.janela_qrcode.mainloop()

    def fechar_janela_qrcode(self):
        if self.janela_qrcode:
            self.janela_qrcode.destroy()
            self.janela_qrcode = None

    def fechar_janela_resumo_venda(self):
        if self.janela_resumo:
            self.janela_resumo.destroy()
            self.janela_resumo = None                   

    def finalizar_venda(self):
        periodo_aberto = self.database.obter_periodo_aberto()
        if not periodo_aberto:
            messagebox.showwarning("Período não Iniciado", "Não há período em aberto. Inicie um período antes de cadastrar produtos.")

        # Obter a data e hora atual
        data_venda = datetime.now().strftime("%d-%m-%Y")
        hora_venda = datetime.now().strftime("%H:%M:%S")
        #total Venda
        total_venda = sum(produto["valor_total_produto"] for produto in self.produtos_selecionados)
        tipo_pagamento = self.metodo_pagamento
        periodo_id = periodo_aberto[0]

        print (data_venda)
        print (hora_venda)
        print (total_venda)
        print (periodo_id)
        print (tipo_pagamento)

        # Inserir os dados da venda na tabela Vendas
        venda_id = self.database.inserir_venda(data_venda, hora_venda, total_venda, periodo_id, tipo_pagamento)

        print ("passou")
       
        # Inserir os dados dos produtos vendidos na tabela Produtos
        for produto in self.produtos_selecionados:
            produto_id = produto["ID"]
            quantidade = produto["quantidade"]
            valor_unitario = produto["valor_unitario"]
            valor_total_produto = produto["valor_total_produto"]
            venda_cortesia = "Não"  # Produto não é de cortesia
            print(produto)
            
            # Registra Itens Venda
            self.database.inserir_produto_itens_venda(venda_id, produto_id, quantidade, valor_unitario, valor_total_produto, venda_cortesia)
           
        # Inserir os dados dos produtos de cortesia na tabela Produtos
        for produto_cortesia in self.produtos_cortesia_selecionados:
            produto_id = produto_cortesia["ID"]
            quantidade = produto_cortesia["quantidade"]
            valor_unitario = produto_cortesia["valor_unitario"]
            valor_total_produto = produto_cortesia["valor_total_produto"]
            venda_cortesia = "Sim"  # Produto é de cortesia
            self.database.inserir_produto_itens_venda(venda_id, produto_id, quantidade, valor_unitario, valor_total_produto, venda_cortesia)
            print(produto_cortesia)

        # Exibir mensagem de sucesso e limpar os campos após a venda ser registrada
        messagebox.showinfo("Venda Registrada", "A venda foi registrada com sucesso!")
        self.limpar_campos_vendas_finalizar_periodo()
        self.limpar_vendas_selecionadas()
        self.interface.vendas.limpar_campos_vendas_finalizar_periodo()
        self.interface.vendas.limpar_vendas_selecionadas()
        self.fechar_janela_resumo_venda()
    
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