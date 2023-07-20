import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from estrutura import Estrutura
from produto import Produto
from database import Database

class Interface:
    def __init__(self):
        self.estrutura = Estrutura(self)
        self.produto = Produto(self)
        self.database = Database()

    def fechar_programa(self):
        if messagebox.askokcancel("Fechar Programa", "Deseja realmente sair?"):
            self.janela.destroy()

    def executar(self):
        # Configuração da janela principal
        self.janela = tk.Tk()
        self.janela.title("Gerenciador de Produtos")
        self.janela.geometry("660x800")

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

        self.lista_produtos = tk.Listbox(frame_produtos, height=20, width=40)
        self.lista_produtos.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

         # Frame da direita (300x800)
        frame_direita = tk.Frame(panedwindow, width=330, height=800)
        panedwindow.add(frame_direita)

         # Frame de edição de produtos
        frame_edicao = tk.Frame(frame_direita, highlightthickness=1, highlightbackground="black")
        frame_edicao.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Label "Edição de Produto"
        label_edicao = tk.Label(frame_edicao, text="Edição de Produto:")
        label_edicao.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

         # Label para exibir a data e a hora de cadastro
        self.label_cadastro_info_data = tk.Label(frame_edicao, text="")
        self.label_cadastro_info_data.grid(row=1, column=0, padx=10, pady=0)

         # Label para exibir a data e a hora de cadastro
        self.label_cadastro_info_hora = tk.Label(frame_edicao, text="")
        self.label_cadastro_info_hora.grid(row=2, column=0, padx=10, pady=0)

        # Label de seleção de produto
        label_selecao = tk.Label(frame_edicao, text="Selecionar Produto:")
        label_selecao.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

        # Combobox de seleção de produto
        self.combobox_produtos = ttk.Combobox(frame_edicao)
        self.combobox_produtos.grid(row=3, column=1, padx=10, pady=5)
        self.combobox_produtos.bind("<<ComboboxSelected>>", self.produto.carregar_dados_produto)

        # Campos de edição de produto
        self.label_nome_edicao = tk.Label(frame_edicao, text="Nome:")
        self.label_nome_edicao.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_nome_edicao = tk.Entry(frame_edicao)
        self.entry_nome_edicao.grid(row=4, column=1, padx=10, pady=5)

        self.label_valor_edicao = tk.Label(frame_edicao, text="Valor:")
        self.label_valor_edicao.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_valor_edicao = tk.Entry(frame_edicao)
        self.entry_valor_edicao.grid(row=5, column=1, padx=10, pady=5)

        self.label_quantidade_edicao = tk.Label(frame_edicao, text="Quantidade:")
        self.label_quantidade_edicao.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

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

        # Combobox de produtos para registro de vendas
        label_produtos_venda = tk.Label(frame_vendas, text="Produto:")
        label_produtos_venda.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

        self.combobox_produtos_venda = ttk.Combobox(frame_vendas)
        self.combobox_produtos_venda.grid(row=1, column=1, padx=10, pady=5)
        self.combobox_produtos_venda.bind("<<ComboboxSelected>>", None)

        # Campo de quantidade para registro de vendas
        label_quantidade_venda = tk.Label(frame_vendas, text="Quantidade:")
        label_quantidade_venda.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        self.entry_quantidade_venda = tk.Entry(frame_vendas)
        self.entry_quantidade_venda.grid(row=2, column=1, padx=10, pady=5)

        # Campo de venda cortesia para registro de vendas
        self.venda_cortesia_var = tk.IntVar()
        checkbox_venda_cortesia = tk.Checkbutton(frame_vendas, text="Venda Cortesia", variable=self.venda_cortesia_var)
        checkbox_venda_cortesia.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Configurar evento para fechar o programa
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_programa)

        self.estrutura.showload_status_periodo()  # Verificar o período aberto e exibir produtos
        self.produto.carrega_produtos_combobox()

        self.janela.mainloop()

# Instanciação da interface e execução do programa
interface = Interface()
interface.executar()
