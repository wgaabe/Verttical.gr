import tkinter as tk
from tkinter import messagebox, ttk
from produto import Produto
from estrutura import Estrutura
from controller import Controller
from database import Database
from vendas import Vendas  # Importar a classe Vendas

class Interface:
    def __init__(self):
        # Inicializar a instância de Database
        self.database = Database()

        # Inicializar a instância de Controller, passando a instância de Database
        self.controller = Controller(self.database)
        
        # Definir a interface do controller
        self.controller.interface = self

         # Criar instâncias de Produto e Estrutura, passando a instância de Controller
        self.produto = Produto(self, self.controller)
        self.estrutura = Estrutura(self, self.controller)
        self.vendas = Vendas(self, self.controller)
       

    def fechar_programa(self):
        if messagebox.askokcancel("Fechar Programa", "Deseja realmente sair?"):
            self.janela.destroy()

        
    def executar(self):
        # Configuração da janela principal
        self.janela = tk.Tk()
        self.janela.title("Gerenciador de Produtos")
        self.janela.geometry("660x800")

        self.venda_cortesia = tk.BooleanVar()  # Variável para venda cortesia (checkbox)
        self.venda_cortesia.set(False)  # Valor inicial da venda cortesia (não marcada)

        # Divisão da janela em duas partes
        panedwindow = tk.PanedWindow(self.janela, orient=tk.HORIZONTAL)
        panedwindow.pack(fill=tk.BOTH, expand=True)

        # Frame da esquerda (300x800)
        frame_esquerda = tk.Frame(panedwindow, width=330, height=800)
        panedwindow.add(frame_esquerda)

        # Frame do período
        frame_periodo = tk.Frame(frame_esquerda, highlightthickness=1, highlightbackground="black")
        frame_periodo.grid(row=0, column=0, padx=10, pady=10)

        # Label status período
        self.status_periodo_label = tk.Label(frame_periodo, text="", fg="red")
        self.status_periodo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Botões Iniciar Período e Finalizar Período
        botao_iniciar = tk.Button(frame_periodo, text="Iniciar Período", width=15, command=self.estrutura.iniciar_periodo)
        botao_iniciar.grid(row=1, column=0, padx=10, pady=10)

        botao_finalizar = tk.Button(frame_periodo, text="Finalizar Período", width=15, command=self.estrutura.finalizar_periodo)
        botao_finalizar.grid(row=1, column=1, padx=10, pady=10)

        # Frame de cadastro de produtos
        frame_cadastro = tk.Frame(frame_esquerda, highlightthickness=1, highlightbackground="black")
        frame_cadastro.grid(row=1, column=0, padx=10, pady=10)

        # Campos de cadastro de produto
        label_produtos = tk.Label(frame_cadastro, text="Cadastrar Produtos:")
        label_produtos.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        label_nome = tk.Label(frame_cadastro, text="Nome:")
        label_nome.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_nome = tk.Entry(frame_cadastro)
        self.entry_nome.grid(row=1, column=1, padx=10, pady=5)

        label_valor = tk.Label(frame_cadastro, text="Valor:")
        label_valor.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_valor = tk.Entry(frame_cadastro)
        self.entry_valor.grid(row=2, column=1, padx=10, pady=5)

        label_quantidade = tk.Label(frame_cadastro, text="Quantidade:")
        label_quantidade.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_quantidade = tk.Entry(frame_cadastro)
        self.entry_quantidade.grid(row=3, column=1, padx=10, pady=5)

        botao_cadastrar = tk.Button(frame_cadastro, text="Cadastrar", width=15, command=self.produto.cadastrar_produto)
        botao_cadastrar.grid(row=4, column=1, padx=10, pady=10)

        # Frame de exibição dos produtos cadastrados
        frame_produtos = tk.Frame(frame_esquerda)
        frame_produtos.grid(row=2, column=0, padx=10, pady=10)

        # Tela de exibição dos produtos cadastrados
        self.label_produtos = tk.Label(frame_produtos, text="Produtos cadastrados:")
        self.label_produtos.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.lista_produtos_cadastrados = tk.Frame(frame_produtos, width=10, height=10)
        self.lista_produtos_cadastrados.grid(row=5, column=0, padx=10, pady=5, columnspan=2)

        #self.lista_produtos = tk.Listbox(frame_produtos, height=20, width=40)
        #self.lista_produtos.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

         # Frame da direita (300x800)
        frame_direita = tk.Frame(panedwindow, width=330, height=800)
        panedwindow.add(frame_direita)

         # Frame de edição de produtos
        frame_edicao = tk.Frame(frame_direita, highlightthickness=1, highlightbackground="black")
        frame_edicao.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Label "Edição de Produto"
        label_edicao = tk.Label(frame_edicao, text="Edição de Produto:")
        label_edicao.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

         # Label para exibir a data e a hora de cadastro
        self.label_cadastro_info_data = tk.Label(frame_edicao, text="")
        self.label_cadastro_info_data.grid(row=1, column=0, padx=10, pady=0)

         # Label para exibir a data e a hora de cadastro
        self.label_cadastro_info_hora = tk.Label(frame_edicao, text="")
        self.label_cadastro_info_hora.grid(row=2, column=0, padx=10, pady=0)

        # Label de seleção de produto
        label_selecao = tk.Label(frame_edicao, text="Selecionar Produto:")
        label_selecao.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)

        # Combobox de seleção de produto
        self.combobox_produtos = ttk.Combobox(frame_edicao)
        self.combobox_produtos.grid(row=3, column=1, padx=10, pady=5)
        self.combobox_produtos.bind("<<ComboboxSelected>>", self.produto.carregar_dados_produto)

        # Campos de edição de produto
        self.label_nome_edicao = tk.Label(frame_edicao, text="Nome:")
        self.label_nome_edicao.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_nome_edicao = tk.Entry(frame_edicao)
        self.entry_nome_edicao.grid(row=4, column=1, padx=10, pady=5)

        self.label_valor_edicao = tk.Label(frame_edicao, text="Valor:")
        self.label_valor_edicao.grid(row=5, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_valor_edicao = tk.Entry(frame_edicao)
        self.entry_valor_edicao.grid(row=5, column=1, padx=10, pady=5)

        self.label_quantidade_edicao = tk.Label(frame_edicao, text="Quantidade:")
        self.label_quantidade_edicao.grid(row=6, column=0, padx=10, pady=5, sticky=tk.E)

        self.entry_quantidade_edicao = tk.Entry(frame_edicao)
        self.entry_quantidade_edicao.grid(row=6, column=1, padx=10, pady=5)

        # Botão Salvar
        self.botao_salvar_edicao = tk.Button(frame_edicao, text="Salvar", width=15, command=self.produto.salvar_edicao_produto)
        self.botao_salvar_edicao.grid(row=7, column=1, padx=10, pady=10)

        # Botão Excluir
        self.botao_excluir = tk.Button(frame_edicao, text="Excluir", width=15, command=self.produto.excluir_produto)
        self.botao_excluir.grid(row=7, column=0, padx=10, pady=10)

        # Frame de registro de vendas
        frame_vendas = tk.Frame(frame_direita, highlightthickness=1, highlightbackground="black")
        frame_vendas.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        # Label para exibir o nome do frame de registro de vendas
        label_nome_frame_vendas = tk.Label(frame_vendas, text="Registro de Vendas:")
        label_nome_frame_vendas.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Campo de quantidade para registro de vendas
        self.label_quantidade_venda = tk.Label(frame_vendas, text="", fg="blue")
        self.label_quantidade_venda.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Combobox de produtos para registro de vendas
        label_produtos_venda = tk.Label(frame_vendas, text="Selecionar Produto:")
        label_produtos_venda.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.combobox_produtos_venda = ttk.Combobox(frame_vendas)
        self.combobox_produtos_venda.grid(row=1, column=1, padx=10, pady=5)
        self.combobox_produtos_venda.bind("<<ComboboxSelected>>", self.vendas.atualizar_quantidade_disponivel)

        label_quantidade_venda_label = tk.Label(frame_vendas, text="Quantidade:")
        label_quantidade_venda_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_quantidade_venda = tk.Entry(frame_vendas)
        self.entry_quantidade_venda.grid(row=2, column=1, padx=10, pady=5)

        # Campo de venda cortesia para registro de vendas
        self.venda_cortesia_var = tk.IntVar()
        checkbox_venda_cortesia = tk.Checkbutton(frame_vendas, text="Venda Cortesia", variable=self.venda_cortesia_var)
        checkbox_venda_cortesia.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Botão Adicionar vendas a lista de vendas
        self.botao_adicionar_venda = tk.Button(frame_vendas, text="Adicionar", command=self.adicionar_produto_venda_interface)
        self.botao_adicionar_venda.grid(row=3, column=1, padx=10, pady=5)

        #frame lista de vendas
        # Crie o atributo lista_produtos_venda_tabela aqui dentro do método executar
        self.lista_produtos_venda_tabela = tk.Frame(frame_vendas, width=10, height=0)
        self.lista_produtos_venda_tabela.grid(row=5, column=0, padx=10, pady=5, columnspan=2)

        #botão limpar lista, limpa todos os produtos adicionados
        self.botao_limpar_lista = tk.Button(frame_vendas, text="Limpar Lista", command=self.vendas.limpar_toda_lista_vendas)
        self.botao_limpar_lista.grid(row=6, column=0, padx=10, pady=5, sticky=tk.E)

        # Botão remover produtos da lista 
        self.botao_excluir_venda = tk.Button(frame_vendas, text="Excluir", command=self.vendas.excluir_produto_venda)
        self.botao_excluir_venda.grid(row=6, column=1, padx=10, pady=5)

        # Crie um label para exibir o valor total da venda na interface
        self.label_total_venda = tk.Label(frame_vendas, text="Total da Venda: R$ 0.00")
        self.label_total_venda.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # Botão Registrar Venda
        self.botao_registrar_venda = tk.Button(frame_vendas, text="Registrar Venda", width=15, command=None)
        self.botao_registrar_venda.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        self.criar_tabela_vendas()
        self.criar_tabela_produtos_cadastrados()

        self.atualizar_tabela_produtos_cadastrados()
        self.vendas.carregar_produtos_combobox_venda()
        self.vendas.atualizar_quantidade_disponivel()

        # Configurar evento para fechar o programa
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_programa)

        self.estrutura.showload_status_periodo()  # Verificar o período aberto e exibir produtos
        self.produto.carrega_produtos_combobox()
        
        self.janela.mainloop()

    def criar_tabela_vendas(self):
        self.tabela_vendas = ttk.Treeview(self.lista_produtos_venda_tabela, columns=("Produto", "Quantidade", "Cortesia", "Valor Unitário", "Valor Total"))
        self.tabela_vendas.heading("#0", text="ID")  # Coluna oculta para armazenar o índice do produto na lista
        self.tabela_vendas.heading("Produto", text="Produto")
        self.tabela_vendas.heading("Quantidade", text="Quantidade")
        self.tabela_vendas.heading("Cortesia", text="Cortesia")
        self.tabela_vendas.heading("Valor Unitário", text="Valor Unitário")
        self.tabela_vendas.heading("Valor Total", text="Valor Total")

        self.tabela_vendas.column("#0", stretch=tk.NO, minwidth=0, width=0)  # Coluna oculta
        self.tabela_vendas.column("Produto", anchor=tk.W, width=40)
        self.tabela_vendas.column("Quantidade", anchor=tk.CENTER, width=30)
        self.tabela_vendas.column("Cortesia", anchor=tk.CENTER, width=50)
        self.tabela_vendas.column("Valor Unitário", anchor=tk.CENTER, width=70)
        self.tabela_vendas.column("Valor Total", anchor=tk.CENTER, width=70)

        self.tabela_vendas.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def criar_tabela_produtos_cadastrados(self):
        self.tabela_produtos_cadastrados = ttk.Treeview(self.lista_produtos_cadastrados, columns=("Nome", "Valor", "Quantidade"))
        self.tabela_produtos_cadastrados.heading("#0", text="ID")  # Coluna oculta para armazenar o índice do produto na lista
        self.tabela_produtos_cadastrados.heading("Nome", text="Nome")
        self.tabela_produtos_cadastrados.heading("Valor", text="Valor")
        self.tabela_produtos_cadastrados.heading("Quantidade", text="Quantidade")

        self.tabela_produtos_cadastrados.column("#0", stretch=tk.NO, minwidth=0, width=0)  # Coluna oculta
        self.tabela_produtos_cadastrados.column("Nome", anchor=tk.W, width=70)
        self.tabela_produtos_cadastrados.column("Valor", anchor=tk.CENTER, width=70)
        self.tabela_produtos_cadastrados.column("Quantidade", anchor=tk.CENTER, width=70)

        self.tabela_produtos_cadastrados.grid(row=1, column=0, columnspan=2, padx=10, pady=5)    

    def atualizar_tabela_produtos_cadastrados(self):
        # Limpar a tabela antes de exibir os produtos cadastrados
        for item in self.tabela_produtos_cadastrados.get_children():
            self.tabela_produtos_cadastrados.delete(item)

        # Obter o período aberto (você pode alterar isso dependendo de como está controlando o período aberto)
        periodo_aberto = self.controller.obter_periodo_aberto()

        if periodo_aberto:
            periodo_id = periodo_aberto[0]  # Extrair o primeiro valor do período aberto (que é o ID do período)
            produtos_cadastrados = self.controller.obter_produtos_periodo(periodo_id)

            if produtos_cadastrados:
                # Exibir os produtos na tabela
                for produto in produtos_cadastrados:
                    nome, valor, quantidade = produto[1], produto[2], produto[3]
                    self.tabela_produtos_cadastrados.insert("", tk.END, values=(nome, f"R$ {valor:.2f}", quantidade))
            else:
                # Caso não haja produtos cadastrados para o período aberto, adicione uma mensagem na tabela
                self.tabela_produtos_cadastrados.insert("", tk.END, values=("Nenhum produto cadastrado", "", ""))
        else:
            # Caso não haja período aberto, adicione uma mensagem na tabela
            self.tabela_produtos_cadastrados.insert("", tk.END, values=("Nenhum período aberto", "", ""))


    def adicionar_produto_venda_interface(self):
        produto_selecionado = self.combobox_produtos_venda.get()
        quantidade_selecionada = self.entry_quantidade_venda.get()
        venda_cortesia = self.venda_cortesia_var.get()

        self.vendas.adicionar_produto_venda(produto_selecionado, quantidade_selecionada, venda_cortesia)

        # Limpar campos após adicionar o produto à lista de vendas
        self.label_quantidade_venda.config(text="")
        self.combobox_produtos_venda.set("")
        self.entry_quantidade_venda.delete(0, tk.END)

        self.vendas.atualizar_total_venda()  # Atualiza o valor total da venda na interface

if __name__ == "__main__":
    # Instanciação da interface e execução do programa
    interface = Interface()
    interface.executar()