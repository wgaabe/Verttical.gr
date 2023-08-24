import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from admdata import admdata
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from adm import Administracao
    

class amdlog:

    def __init__(self, adm):
        self.adm = adm
        self.admdata= admdata()

    def carregar_metodos_pagamento(self):
            self.adm.listbox_metodos.delete(0, tk.END)
            metodos_pagamento = self.admdata.obter_metodos_pagamento()

            for metodo in metodos_pagamento:
                self.adm.listbox_metodos.insert(tk.END, f"{metodo[0]} - {metodo[1]} - Taxa: {metodo[2]}")
    
    def cadastrar_metodo_pagamento(self):
        cadastrar_window = tk.Toplevel()
        cadastrar_window.title("Cadastrar Método de Pagamento")

        width = 400
        height = 250
        x = (1920 - width) // 2
        y = (1080 - height) // 2

        cadastrar_window.geometry(f"{width}x{height}+{x}+{y}")

        label_nome = ttk.Label(cadastrar_window, text="Nome do Método:")
        label_nome.pack(padx=10, pady=5)

        entry_nome = ttk.Entry(cadastrar_window)
        entry_nome.pack(padx=10, pady=5)

        label_taxa = ttk.Label(cadastrar_window, text="Taxa do Banco (%):")
        label_taxa.pack(padx=10, pady=5)

        entry_taxa = ttk.Entry(cadastrar_window)
        entry_taxa.pack(padx=10, pady=5)

        def cadastrar():
            nome_metodo = entry_nome.get()
            taxa_banco = entry_taxa.get()

            if nome_metodo and taxa_banco:
                try:
                    taxa_banco = float(taxa_banco)
                    self.admdata.cadastrar_metodo_pagamento(nome_metodo, taxa_banco)
                    messagebox.showinfo("Cadastro", "Método de pagamento cadastrado com sucesso.")
                    self.carregar_metodos_pagamento()  # Atualiza a lista de métodos após o cadastro
                    cadastrar_window.destroy()
                except ValueError:
                    messagebox.showerror("Erro", "Taxa do banco deve ser um número válido.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao cadastrar método de pagamento: {str(e)}")

        botao_cadastrar = ttk.Button(cadastrar_window, text="Cadastrar", command=cadastrar)
        botao_cadastrar.pack(padx=10, pady=10)
    def editar_metodo_pagamento(self):
        # Implemente a função para editar um método de pagamento existente
        pass
    def excluir_metodo_pagamento(self):
        # Implemente a função para excluir um método de pagamento
        pass

    def carregar_periodos(self):
        data_inicio = self.adm.data_inicio.get_date()
        data_fim = self.adm.data_fim.get_date()
        print(data_fim)
        print(data_inicio)

        #data_inicio_formatada = data_inicio.strftime('%d-%m-%Y')
        #data_fim_formatada = data_fim.strftime('%d-%m-%Y')

        #periodos = self.admdata.obter_periodos_entre_datas(data_inicio_formatada, data_fim_formatada)
        periodos = self.admdata.obter_periodos_entre_datas(data_inicio, data_fim)
        
        # Atualize a ComboBox com os períodos
        self.adm.combobox_periodo.set("")
        self.adm.combobox_periodo["values"] = periodos
        
        # Atualize a Label com a quantidade de registros
        qtd_registros = len(periodos)
        self.adm.label_qtd_registros.config(text=f"Quantidade de Registros: {qtd_registros}")

    def gerar_relatorio(self):
        tipo_relatorio = self.adm.combobox_tipo_relatorio.get()

        if not self.adm.combobox_periodo.get():  # Verifica se o período não está vazio
            messagebox.showerror("Erro", "Selecione um período antes de gerar o relatório.")
            return

        if tipo_relatorio == "Vendas por Hora":
            relatorio = self.gerar_relatorio_vendas_por_hora()
        elif tipo_relatorio == "Outro Tipo de Relatório":
            relatorio = self.gerar_outro_tipo_de_relatorio()
        else:
            relatorio = "Tipo de relatório não suportado."

    def gerar_relatorio_vendas_por_hora(self):
        periodo_selecionado = self.adm.combobox_periodo.get()
        periodo_id = int(periodo_selecionado.split()[0])  # Obtém o ID do período

        vendas_por_hora = self.admdata.obter_quantidade_vendas_por_hora(periodo_id)
        print(vendas_por_hora)
        # Cria uma lista com todas as horas do período, incluindo a transição de um dia para outro
        horas_do_periodo = [f"{i:02d}:00" for i in range(24)] + [f"{i:02d}:00" for i in range(24)]

        quantidades = [vendas_por_hora.get(hora, 0) for hora in horas_do_periodo]  # Preenche quantidades com 0 se não houver vendas

        # Criação do gráfico de barras
        plt.bar(horas_do_periodo, quantidades)
        plt.xlabel("Hora")
        plt.ylabel("Quantidade de Vendas")
        plt.title("Vendas por Hora")
        plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo x para melhor visualização

        # Adiciona o valor da quantidade de vendas acima de cada barra
        for i, v in enumerate(quantidades):
            plt.text(i, v + 0.1, str(v), ha='center')

        # Exibe o gráfico em uma janela do sistema
        plt.show()