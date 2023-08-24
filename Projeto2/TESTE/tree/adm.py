import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from admdata import admdata
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from admlog import amdlog
from admcontroller import AdmController

class Administracao:
   def __init__(self, root):
        self.admdata = admdata()
        self.admlog = amdlog(self)

        style = ttk.Style()
        style.configure("Custom.TButton", font=("Helvetica", 12), padding=5)
        style.configure("Custom.TLabel", font=("Helvetica", 12))
        style.configure("Custom.TCombobox", font=("Helvetica", 12), fieldbackground="white", padding=5)
        fonte_default = (12)

        self.root = root
        self.root.title("Administração - Relatórios de Vendas")
        self.root.geometry("1920x1080")

        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(padx=20, pady=20, anchor="center")

        self.frame_filtros = tk.LabelFrame(self.frame_principal, text="Relatórios", font="Custom.TLabel")
        self.frame_filtros.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

        self.label_data_inicio = ttk.Label(self.frame_filtros, text="Data de Início:", style="Custom.TLabel")
        self.label_data_inicio.grid(row=0, column=0, padx=5, pady=5)

        self.data_inicio = DateEntry(self.frame_filtros, width=12, style="Custom.TCombobox")
        self.data_inicio.grid(row=0, column=1, padx=5, pady=5)

        self.label_data_fim = ttk.Label(self.frame_filtros, text="Data de Fim:", style="Custom.TLabel")
        self.label_data_fim.grid(row=0, column=2, padx=5, pady=5)

        self.data_fim = DateEntry(self.frame_filtros, width=12, style="Custom.TCombobox")
        self.data_fim.grid(row=0, column=3, padx=5, pady=5)

        self.carregar_button = ttk.Button(self.frame_filtros, text="Carregar Períodos", style="Custom.TButton", command=self.admlog.carregar_periodos)
        self.carregar_button.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)

        self.config_frame = ttk.Frame(self.frame_filtros, borderwidth=2, relief="solid")
        self.config_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=15, sticky=tk.W)

        self.label_qtd_registros = ttk.Label(self.config_frame, text="Quantidade de Registros:", style="Custom.TLabel")
        self.label_qtd_registros.pack(side=tk.LEFT, padx=5)

        self.combobox_periodo = ttk.Combobox(self.config_frame, state="readonly", style="Custom.TCombobox", width=30)
        self.combobox_periodo.pack(side=tk.LEFT, padx=5)

        self.label_tipo_relatorio = ttk.Label(self.config_frame, text="Relatório:", style="Custom.TLabel")
        self.label_tipo_relatorio.pack(side=tk.LEFT, padx=5)

        self.combobox_tipo_relatorio = ttk.Combobox(self.config_frame, state="readonly", style="Custom.TCombobox", width=20)
        self.combobox_tipo_relatorio.pack(side=tk.LEFT, padx=5)

        tipos_relatorio = ["Vendas por Hora", "Outro Tipo de Relatório"]
        self.combobox_tipo_relatorio["values"] = tipos_relatorio

        self.gerar_relatorio_button = ttk.Button(self.config_frame, text="Gerar Relatório", style="Custom.TButton", command=self.admlog.gerar_relatorio)
        self.gerar_relatorio_button.pack(side=tk.LEFT, padx=5)

        # Seção de Taxas de Pagamento
        self.taxas_pagamento_frame = tk.LabelFrame(self.frame_principal, text="Taxas Pagamento", font="Custom.TLabel")
        self.taxas_pagamento_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ne")  # Ajuste posição e espaçamento

        self.treeview_metodos = ttk.Treeview(self.taxas_pagamento_frame, columns=("ID", "Nome", "Taxa"), show="headings", height=5)
        self.treeview_metodos.heading("ID", text="ID")
        self.treeview_metodos.heading("Nome", text="Nome")
        self.treeview_metodos.heading("Taxa", text="Taxa")

        self.treeview_metodos.column("ID", width=50)
        self.treeview_metodos.column("Nome", width=150)
        self.treeview_metodos.column("Taxa", width=100)

        self.scrollbar_metodos = ttk.Scrollbar(self.taxas_pagamento_frame, orient=tk.VERTICAL, command=self.treeview_metodos.yview)
        self.scrollbar_metodos.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview_metodos.configure(yscrollcommand=self.scrollbar_metodos.set)

        self.treeview_metodos.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        self.botao_frame = ttk.Frame(self.taxas_pagamento_frame)
        self.botao_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.Y)

        self.botao_cadastrar = ttk.Button(self.botao_frame, text="Cadastrar", command=self.admlog.cadastrar_metodo_pagamento, style="Custom.TButton")
        self.botao_cadastrar.pack(side=tk.TOP, padx=5, pady=2, fill=tk.X)

        self.botao_editar = ttk.Button(self.botao_frame, text="Editar", command=self.admlog.editar_metodo_pagamento, style="Custom.TButton")
        self.botao_editar.pack(side=tk.TOP, padx=5, pady=2, fill=tk.X)

        self.botao_excluir = ttk.Button(self.botao_frame, text="Excluir", command=self.admlog.excluir_metodo_pagamento, style="Custom.TButton")
        self.botao_excluir.pack(side=tk.TOP, padx=5, pady=2, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = Administracao(root)
    root.mainloop()
