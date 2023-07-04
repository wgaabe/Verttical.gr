import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from datetime import datetime
import csv
import os


class Produto:
    def __init__(self, data, hora, nome_produto, valor_venda, quantidade_estoque, quantidade_vendida, venda_cortesia):
        self.data = data
        self.hora = hora
        self.nome_produto = nome_produto
        self.valor_venda = valor_venda
        self.quantidade_estoque = quantidade_estoque
        self.quantidade_vendida = quantidade_vendida
        self.venda_cortesia = venda_cortesia


class SistemaControleVendas:
    def __init__(self):
        self.produtos = []
        self.valor_total_vendas = 0.0  # Variável para armazenar o valor total das vendas
        self.quantidade_vendida = 0
        self.venda_cortesia = 0
        #self.verifica_venda_cortesia = False
        self.data = None
        self.arquivo = None
    

        self.janela = tk.Tk()
        self.janela.title("Controle de Vendas")
        self.verifica_venda_cortesia = tk.BooleanVar()
        self.frame_lista_produtos = None

        self.frame_arquivos_status = tk.Frame(self.janela)
        self.frame_arquivos_status.pack()

        # Estilo do label
        estilo_caminho_arquivo = ("Arial", 8, "bold")

        # Criação do label dentro do frame_arquivos_status
        self.label_caminho_arquivo = tk.Label(self.frame_arquivos_status, text="Caminho do arquivo: (nenhum arquivo selecionado)",
                                            font=estilo_caminho_arquivo)
        self.label_caminho_arquivo.grid(row=0, column=1, padx=5, pady=5,)
        self.label_caminho_arquivo.bind("<Button-1>", self.abrir_diretorio)

        # Criação do botão Carregar Período dentro do frame_arquivos_status
        self.btn_carregar_periodo = tk.Button(self.frame_arquivos_status, text="Carregar Período", command=self.carregar_periodo)
        self.btn_carregar_periodo.grid(row=1, column=1, padx=(10,130))

        # Criação do botão Gerar Período dentro do frame_arquivos_status
        self.btn_gerar_periodo = tk.Button(self.frame_arquivos_status, text="Gerar Período", command=self.gerar_periodo)
        self.btn_gerar_periodo.grid(row=1, column=1, padx=(130,10))

        self.frame_cadastro = tk.Frame(self.janela)
        self.frame_cadastro.pack(padx=10, pady=10)

        self.label_cadastro_titulo = tk.Label(self.frame_cadastro, text="Cadastro de Produto")
        self.label_cadastro_titulo.grid(row=1, columnspan=2, padx=5, pady=5)

        self.label_nome = tk.Label(self.frame_cadastro, text="Nome:")
        self.label_nome.grid(row=2, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(self.frame_cadastro)
        self.entry_nome.grid(row=2, column=1, padx=5, pady=5)

        self.label_valor = tk.Label(self.frame_cadastro, text="Valor:")
        self.label_valor.grid(row=3, column=0, padx=5, pady=5)
        self.entry_valor = tk.Entry(self.frame_cadastro)
        self.entry_valor.grid(row=3, column=1, padx=5, pady=5)

        self.label_quantidade = tk.Label(self.frame_cadastro, text="Quantidade:")
        self.label_quantidade.grid(row=4, column=0, padx=5, pady=5)
        self.entry_quantidade = tk.Entry(self.frame_cadastro)
        self.entry_quantidade.grid(row=4, column=1, padx=5, pady=5)

        self.btn_cadastrar = tk.Button(self.frame_cadastro, text="Cadastrar", command=self.cadastrar_produto)
        self.btn_cadastrar.grid(row=5, columnspan=2, padx=5, pady=5)

        self.frame_edicao = tk.Frame(self.janela)
        self.frame_edicao.pack(padx=10, pady=10)

        self.label_edicao_titulo = tk.Label(self.frame_edicao, text="Edição de Produto")
        self.label_edicao_titulo.grid(row=0, columnspan=2, padx=5, pady=5)    

        self.label_produto_editar = tk.Label(self.frame_edicao, text="Produto:")
        self.label_produto_editar.grid(row=1, column=0, padx=5, pady=5)
        self.combobox_produtos_editar = ttk.Combobox(self.frame_edicao, values=[], state="readonly")
        self.combobox_produtos_editar.grid(row=1, column=1, padx=5, pady=5)
        self.combobox_produtos_editar.bind("<<ComboboxSelected>>", self.preencher_campos_edicao)

        self.label_nome_editar = tk.Label(self.frame_edicao, text="Nome:")
        self.label_nome_editar.grid(row=2, column=0, padx=5, pady=5)
        self.entry_nome_editar = tk.Entry(self.frame_edicao)
        self.entry_nome_editar.grid(row=2, column=1, padx=5, pady=5)

        self.label_valor_editar = tk.Label(self.frame_edicao, text="Valor:")
        self.label_valor_editar.grid(row=3, column=0, padx=5, pady=5)
        self.entry_valor_editar = tk.Entry(self.frame_edicao)
        self.entry_valor_editar.grid(row=3, column=1, padx=5, pady=5)

        self.label_quantidade_editar = tk.Label(self.frame_edicao, text="Quantidade:")
        self.label_quantidade_editar.grid(row=4, column=0, padx=5, pady=5)
        self.entry_quantidade_editar = tk.Entry(self.frame_edicao)
        self.entry_quantidade_editar.grid(row=4, column=1, padx=5, pady=5)

        self.btn_excluir = tk.Button(self.frame_edicao, text="Excluir", command=self.excluir_produto)
        self.btn_excluir.grid(row=5, column=0, padx=5, pady=5)

        self.btn_editar = tk.Button(self.frame_edicao, text="Editar", command=self.editar_produto)
        self.btn_editar.grid(row=5, column=1, padx=5, pady=5)

        self.frame_venda = tk.Frame(self.janela)
        self.frame_venda.pack(padx=10, pady=10)

        self.label_venda_titulo = tk.Label(self.frame_venda, text="Venda de Produto")
        self.label_venda_titulo.grid(row=0, columnspan=2, padx=5, pady=5)

        self.label_produto_venda = tk.Label(self.frame_venda, text="Produto:")
        self.label_produto_venda.grid(row=1, column=0, padx=5, pady=5)
        self.combobox_produtos_venda = ttk.Combobox(self.frame_venda, values=[], state="readonly")
        self.combobox_produtos_venda.grid(row=1, column=1, padx=5, pady=5)

        self.label_quantidade_venda = tk.Label(self.frame_venda, text="Quantidade:")
        self.label_quantidade_venda.grid(row=2, column=0, padx=5, pady=5)
        self.entry_quantidade_venda = tk.Entry(self.frame_venda)
        self.entry_quantidade_venda.grid(row=2, column=1, padx=5, pady=5)
            
        self.checkbutton_venda_cortesia = tk.Checkbutton(
        self.frame_venda,
        text="Venda Cortesia",
        variable=self.verifica_venda_cortesia
        )
        self.checkbutton_venda_cortesia.grid(row=3, column=0, padx=5, pady=5)    
            
        self.btn_vender = tk.Button(self.frame_venda, text="Vender", command=self.realizar_venda)
        self.btn_vender.grid(row=3, column=1, padx=5, pady=5)
        

        self.frame_lista_produtos = tk.Frame(self.janela)
        self.frame_lista_produtos.pack(padx=10, pady=10)

        self.label_lista_produtos = tk.Label(self.frame_lista_produtos, text="Produtos Cadastrados:")
        self.label_lista_produtos.grid(row=0, column=0, padx=5, pady=5)

        self.text_lista_produtos = tk.Text(self.frame_lista_produtos, width=40, height=10)
        self.text_lista_produtos.grid(row=1, column=0, padx=5, pady=5)

        # Adicione a barra de rolagem vertical
        scrollbar = tk.Scrollbar(self.frame_lista_produtos, command=self.text_lista_produtos.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")

        # Configure a barra de rolagem para controlar a exibição do texto
        self.text_lista_produtos.config(yscrollcommand=scrollbar.set)

        self.label_valor_total_vendas = tk.Label(self.frame_lista_produtos, text="Valor Total das Vendas: R$ 0.00")
        self.label_valor_total_vendas.grid(row=2, column=0, padx=5, pady=5)

        self.btn_gerar_relatorio = tk.Button(self.frame_lista_produtos, text="Gerar Relatório", command=None)
        self.btn_gerar_relatorio.grid(row=3, column=0, padx=5, pady=5)

        self.atualizar_combobox_produtos()

        self.janela.mainloop()

    def cadastrar_produto(self):
        if not hasattr(self, 'arquivo') or self.arquivo is None:
            tk.messagebox.showerror("Erro", "Nenhum arquivo Selecionado! Gere um novo período ou carregue o período!")
            return
        nome = self.entry_nome.get()
        valor = self.entry_valor.get()
        quantidade = self.entry_quantidade.get()
        #venda_cortesia = self.verifica_venda_cortesia.get()


        if nome and valor and quantidade:
            if self.is_float(valor) and self.is_int(quantidade):
                data_hora_atual = datetime.now()
                data = data_hora_atual.strftime("%d/%m/%Y")
                hora = data_hora_atual.strftime("%H:%M")

                produto = Produto(data, hora, nome, float(valor), int(quantidade), 0, 0)
                self.produtos.append(produto)
                self.limpar_campos()
                self.atualizar_combobox_produtos()
                self.exibir_lista_produtos()
                tk.messagebox.showinfo("Cadastro de Produto", "Produto cadastrado com sucesso!")
                
                # Atualizar o arquivo CSV
                self.atualizar_arquivo_csv()
            else:
                tk.messagebox.showerror("Erro de Cadastro", "Valor ou quantidade inválidos!")
        else:
            tk.messagebox.showerror("Erro de Cadastro", "Preencha todos os campos!")

    def editar_produto(self):
        produto_index = self.combobox_produtos_editar.current()

        if produto_index >= 0:
            nome = self.entry_nome_editar.get()
            valor = self.entry_valor_editar.get()
            quantidade = self.entry_quantidade_editar.get()

            if nome and valor and quantidade:
                if self.is_float(valor) and self.is_int(quantidade):
                    produto = self.produtos[produto_index]
                    produto["nome"] = nome
                    produto["valor"] = float(valor)
                    produto["quantidade"] = int(quantidade)
                    self.limpar_campos_edicao()
                    self.atualizar_combobox_produtos()
                    self.exibir_lista_produtos()
                    tk.messagebox.showinfo("Edição de Produto", "Produto editado com sucesso!")
                    self.atualizar_arquivo_csv()
                else:
                    tk.messagebox.showerror("Erro de Edição", "Valor ou quantidade inválidos!")
            else:
                tk.messagebox.showerror("Erro de Edição", "Preencha todos os campos!")
        else:
            tk.messagebox.showerror("Erro de Edição", "Nenhum produto selecionado!")

    def excluir_produto(self):
        produto_index = self.combobox_produtos_editar.current()

        if produto_index >= 0:
            produto = self.produtos[produto_index]
            confirmacao = tk.messagebox.askyesno("Confirmação de Exclusão", f"Deseja excluir o produto '{produto['nome']}'?")
            if confirmacao:
                self.produtos.pop(produto_index)
                self.limpar_campos_edicao()
                self.atualizar_combobox_produtos()
                self.exibir_lista_produtos()
                tk.messagebox.showinfo("Exclusão de Produto", "Produto excluído com sucesso!")
                self.atualizar_arquivo_csv()
            else:
                tk.messagebox.showinfo("Cancelado", "A exclusão do produto foi cancelada.")
        else:
            tk.messagebox.showerror("Erro de Exclusão", "Nenhum produto selecionado!")

    def realizar_venda(self):
        if self.arquivo:
            produto_index = self.combobox_produtos_venda.current()
            quantidade_venda = self.entry_quantidade_venda.get()
            #venda_cortesia = self.checkbutton_venda_cortesia.get()  # Obtém o estado da caixa de seleção

            if produto_index >= 0 and quantidade_venda:
                if self.is_int(quantidade_venda):
                    produto = self.produtos[produto_index]
                    quantidade_venda = int(quantidade_venda)

                    if quantidade_venda <= produto.quantidade_estoque:
                        if not hasattr(produto, 'quantidade_vendida'):
                            produto.quantidade_vendida = 0
                        produto.quantidade_estoque -= quantidade_venda
                        produto.quantidade_vendida += quantidade_venda
                        self.quantidade_vendida += quantidade_venda
                        if self.verifica_venda_cortesia.get() and quantidade_venda > 0:  # Verifica se a opção "Venda Cortesia" está marcada e a quantidade vendida é maior que zero
                            produto.venda_cortesia += 1
                        else:
                            self.valor_total_vendas += produto.valor_venda * quantidade_venda
                        self.atualizar_combobox_produtos()
                        self.exibir_lista_produtos()
                        self.exibir_valor_total_vendas()
                        tk.messagebox.showinfo("Venda de Produto", "Venda realizada com sucesso!")
                        print("Quantidade vendida:", self.quantidade_vendida)

                        self.entry_quantidade_venda.delete(0, tk.END)

                        with open(self.arquivo, 'a', newline='') as arquivo_csv:
                            writer = csv.writer(arquivo_csv)
                            for produto in self.produtos:
                                nome = produto.nome_produto
                                valor = produto.valor_venda
                                quantidade = produto.quantidade_estoque
                                vendas_cortesia = produto.venda_cortesia
                                writer.writerow([nome, valor, quantidade, vendas_cortesia])

                    else:
                        tk.messagebox.showerror("Erro de Venda", "Quantidade indisponível em estoque!")
                else:
                    tk.messagebox.showerror("Erro de Venda", "Quantidade inválida!")
            else:
                tk.messagebox.showerror("Erro de Venda", "Selecione um produto e informe a quantidade!")
        else:
            tk.messagebox.showerror("Erro", "Nenhum arquivo CSV selecionado!")



   

    def exibir_valor_total_vendas(self):
        self.label_valor_total_vendas.config(text=f"Valor Total das Vendas: R$ {self.valor_total_vendas:.2f}")

    def atualizar_combobox_produtos(self):
        produtos = [produto.nome_produto for produto in self.produtos]
        self.combobox_produtos_editar["values"] = produtos
        self.combobox_produtos_venda["values"] = produtos

    def exibir_lista_produtos(self):
        self.text_lista_produtos.delete("1.0", tk.END)
        for produto in self.produtos:
            texto = f"Nome: {produto.nome_produto}\n"
            texto += f"Valor: R$ {produto.valor_venda}\n"
            texto += f"Quantidade em Estoque: {produto.quantidade_estoque}\n"
            texto += f"Quantidade Vendida: {produto.quantidade_vendida}\n"
            texto += f"Vendas Cortesia: {produto.venda_cortesia}\n"  # Acesso direto ao atributo venda_cortesia
            texto += "=========================\n"
            self.text_lista_produtos.insert(tk.END, texto)


    def preencher_campos_edicao(self, event):
        produto_index = self.combobox_produtos_editar.current()

        if produto_index >= 0:
            produto = self.produtos[produto_index]
            self.entry_nome_editar.delete(0, tk.END)
            self.entry_nome_editar.insert(tk.END, produto["nome"])
            self.entry_valor_editar.delete(0, tk.END)
            self.entry_valor_editar.insert(tk.END, produto["valor"])
            self.entry_quantidade_editar.delete(0, tk.END)
            self.entry_quantidade_editar.insert(tk.END, produto["quantidade"])

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.entry_quantidade.delete(0, tk.END)

    def limpar_campos_edicao(self):
        self.combobox_produtos_editar.set('')
        self.entry_nome_editar.delete(0, tk.END)
        self.entry_valor_editar.delete(0, tk.END)
        self.entry_quantidade_editar.delete(0, tk.END)

    def atualizar_arquivo_csv(self):
        if self.arquivo:
            with open(self.arquivo, 'w', newline='') as arquivo_csv:
                writer = csv.writer(arquivo_csv)
                data_hora_atual = datetime.now()
                data = data_hora_atual.strftime("%d/%m/%Y")
                hora = data_hora_atual.strftime("%H:%M")
                writer.writerow(["Data", "Hora", "Nome", "Valor Venda", "Quantidade Estoque", "Quantidade Vendida", "Venda Cortesia"])
                for produto in self.produtos:
                    data = produto.data
                    hora = produto.hora
                    nome = produto.nome_produto
                    valor = produto.valor_venda
                    quantidade = produto.quantidade_estoque
                    vendas = produto.quantidade_vendida
                    cortesia = produto.venda_cortesia
                    writer.writerow([data, hora, nome, valor, quantidade, vendas, cortesia])
        else:
            tk.messagebox.showerror("Erro", "Nenhum arquivo selecionado!")


    def carregar_periodo(self):
        arquivo = filedialog.askopenfilename(filetypes=[("Arquivo CSV", "*.csv")])
        if arquivo:
            with open(arquivo, 'r') as arquivo_csv:
                reader = csv.reader(arquivo_csv)
                self.produtos.clear()  # Limpar a lista de produtos existentes
                next(reader)  # Pular o cabeçalho do CSV
                for linha in reader:
                    data = linha[0]
                    hora = linha[1]
                    nome = linha[2]
                    valor = float(linha[3])
                    quantidade = int(linha[4])
                    vendas = int(linha[5])
                    cortesia = int(linha[6])
                    produto = Produto(data, hora, nome, valor, quantidade, vendas, cortesia)
                    self.produtos.append(produto)

            # Atualizar os valores totais
            self.valor_total_vendas = sum(produto.valor_venda * produto.quantidade_vendida for produto in self.produtos)
            self.quantidade_vendida = sum(produto.quantidade_vendida for produto in self.produtos)
            self.vendas_cortesia = sum(produto.venda_cortesia for produto in self.produtos)

            # Exibir a lista de produtos
            self.exibir_lista_produtos()

            # Exibir o caminho do arquivo
            self.exibir_diretorio_arquivo(arquivo)

            self.atualizar_combobox_produtos()

        else:
            tk.messagebox.showerror("Erro", "Nenhum arquivo selecionado!")

    def gerar_periodo(self):
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Arquivo CSV", "*.csv")])
        if arquivo:
            with open(arquivo, 'w', newline='') as arquivo_csv:
                writer = csv.writer(arquivo_csv)
                writer.writerow(["Data","Hora", "Nome", "Valor Venda", "Quantidade Estoque", "Quantidade Vendida", "Venda Cortesia"])
                for produto in self.produtos:
                    data = produto.data
                    hora = produto.hora
                    nome = produto.nome_produto
                    valor = produto.valor_venda
                    quantidade = produto.quantidade_estoque
                    vendas = produto.quantidade_vendida
                    cortesia = produto.venda_cortesia
                    writer.writerow([data, hora, nome, valor, quantidade, vendas, cortesia])

            # Exibir o caminho do arquivo
            self.exibir_diretorio_arquivo(arquivo)

        else:
            tk.messagebox.showerror("Erro", "Nenhum arquivo selecionado!")

    def abrir_diretorio(self, event):
        if self.arquivo:
            pasta = os.path.dirname(self.arquivo)  # Obtém o diretório do arquivo
            os.startfile(pasta)

    def exibir_diretorio_arquivo(self, caminho):
        self.arquivo = caminho
        self.label_caminho_arquivo.config(text="Caminho do arquivo: " + caminho)


    def is_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def is_int(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False


if __name__ == "__main__":
    sistema = SistemaControleVendas()