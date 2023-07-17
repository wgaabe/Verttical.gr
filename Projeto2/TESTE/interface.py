import tkinter as tk
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
        self.janela.geometry("300x800")

        # Frame do período
        frame_periodo = tk.Frame(self.janela)
        frame_periodo.grid(padx=10, pady=10)

        # Label status período
        self.status_periodo_label = tk.Label(frame_periodo, text="", fg="red")
        self.status_periodo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky=tk.W)

        # Botões Iniciar Período e Finalizar Período
        botao_iniciar = tk.Button(frame_periodo, text="Iniciar Período", width=15, command=self.estrutura.iniciar_periodo)
        botao_iniciar.grid(row=1, column=0, padx=10, pady=10)

        botao_finalizar = tk.Button(frame_periodo, text="Finalizar Período", width=15, command=self.estrutura.finalizar_periodo)
        botao_finalizar.grid(row=1, column=1, padx=10, pady=10)

        # Frame de cadastro de produtos
        frame_cadastro = tk.Frame(self.janela)
        frame_cadastro.grid(padx=10, pady=10)

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
        frame_produtos = tk.Frame(self.janela)
        frame_produtos.grid(padx=10, pady=10)

        # Tela de exibição dos produtos cadastrados
        self.label_produtos = tk.Label(frame_produtos, text="Produtos cadastrados:")
        self.label_produtos.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.lista_produtos = tk.Listbox(frame_produtos, height=20, width=40)
        self.lista_produtos.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

        self.botao_editar = tk.Button(frame_produtos, text="Editar", width=15, command=self.produto.editar_produto)
        self.botao_editar.grid(row=2, column=1, padx=10, pady=10)

        # Botão Vendas
        self.botao_vendas = tk.Button(frame_produtos, text="Vendas", width=15, command=self.estrutura.registrar_venda)
        self.botao_vendas.grid(row=2, column=0, padx=10, pady=10)

        # Configurar evento para fechar o programa
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_programa)

        self.estrutura.showload_status_periodo()  # Verificar o período aberto e exibir produtos

        self.janela.mainloop()

# Instanciação da interface e execução do programa
interface = Interface()
interface.executar()
