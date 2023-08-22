import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from admlog import admlog
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Administracao:
    def __init__(self, root):
        self.admlog = admlog()

        style = ttk.Style()
        style.configure("Customadm.TCombobox", font=30, fieldbackground="white", padding=5)

        self.root = root
        self.root.title("Administração - Relatórios de Vendas")
        self.root.geometry("800x600")

        self.frame_filtros = ttk.Frame(self.root, borderwidth=2, relief="solid")
        self.frame_filtros.pack(padx=10, pady=10)

        self.label_data_inicio = ttk.Label(self.frame_filtros, text="Data de Início:")
        self.label_data_inicio.grid(row=0, column=0, padx=5, pady=5)

        self.data_inicio = DateEntry(self.frame_filtros, width=12)
        self.data_inicio.grid(row=0, column=1, padx=5, pady=5)

        self.label_data_fim = ttk.Label(self.frame_filtros, text="Data de Fim:")
        self.label_data_fim.grid(row=0, column=2, padx=5, pady=5)

        self.data_fim = DateEntry(self.frame_filtros, width=12)
        self.data_fim.grid(row=0, column=3, padx=5, pady=5)

        self.carregar_button = ttk.Button(self.frame_filtros, text="Carregar Períodos", command=self.carregar_periodos)
        self.carregar_button.grid(row=0, column=4, padx=5, pady=5)

        self.config_frame = ttk.Frame(self.frame_filtros, borderwidth=2, relief="solid")
        self.config_frame.grid(row=1, column=0, columnspan=5, padx=5, pady=5)

        self.label_qtd_registros = ttk.Label(self.config_frame, text="Quantidade de Registros:")
        self.label_qtd_registros.pack(side=tk.LEFT, padx=5)

        self.combobox_periodo = ttk.Combobox(self.config_frame, state="readonly", style="Customadm.TCombobox", width=40)
        self.combobox_periodo.pack(side=tk.LEFT, padx=5)

        self.label_tipo_relatorio = ttk.Label(self.config_frame, text="Relatorio:")
        self.label_tipo_relatorio.pack(side=tk.LEFT, padx=5)

        self.combobox_tipo_relatorio = ttk.Combobox(self.config_frame, state="readonly", style="Customadm.TCombobox", width=20)
        self.combobox_tipo_relatorio.pack(side=tk.LEFT, padx=5)

         # Adicione as opções de tipo de relatório à combobox
        tipos_relatorio = ["Vendas por Hora", "Outro Tipo de Relatório"]
        self.combobox_tipo_relatorio["values"] = tipos_relatorio

        self.gerar_relatorio_button = ttk.Button(self.config_frame, text="Gerar Relatório", command=self.gerar_relatorio)
        self.gerar_relatorio_button.pack(side=tk.LEFT, padx=5)

        self.frame_relatorio = ttk.Frame(self.root)
        self.frame_relatorio.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        #self.text_relatorio = tk.Text(self.frame_relatorio, wrap=tk.WORD)
        #self.text_relatorio.pack(fill=tk.BOTH, expand=True)

    def carregar_periodos(self):
        data_inicio = self.data_inicio.get_date()
        data_fim = self.data_fim.get_date()
        print(data_fim)

        data_inicio_formatada = data_inicio.strftime('%d-%m-%Y')
        data_fim_formatada = data_fim.strftime('%d-%m-%Y')

        #periodos = self.admlog.obter_periodos_entre_datas(data_inicio_formatada, data_fim_formatada)
        periodos = self.admlog.obter_periodos_entre_datas(data_inicio, data_fim)
        
        # Atualize a ComboBox com os períodos
        self.combobox_periodo["values"] = periodos
        
        # Atualize a Label com a quantidade de registros
        qtd_registros = len(periodos)
        self.label_qtd_registros.config(text=f"Quantidade de Registros: {qtd_registros}")

    def gerar_relatorio(self):
        tipo_relatorio = self.combobox_tipo_relatorio.get()

        if tipo_relatorio == "Vendas por Hora":
            relatorio = self.gerar_relatorio_vendas_por_hora()
        elif tipo_relatorio == "Outro Tipo de Relatório":
            relatorio = self.gerar_outro_tipo_de_relatorio()
        else:
            relatorio = "Tipo de relatório não suportado."

    def gerar_relatorio_vendas_por_hora(self):
        periodo_selecionado = self.combobox_periodo.get()
        periodo_id = int(periodo_selecionado.split()[0])  # Obtém o ID do período

        vendas_por_hora = self.admlog.obter_quantidade_vendas_por_hora(periodo_id)

        horas = []
        quantidades = []

        for hora, quantidade in vendas_por_hora.items():
            horas.append(hora)
            quantidades.append(quantidade)

        # Criação do gráfico de barras
        plt.bar(horas, quantidades)
        plt.xlabel("Hora")
        plt.ylabel("Quantidade de Vendas")
        plt.title("Vendas por Hora")
        plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo x para melhor visualização

        # Adiciona o valor da quantidade de vendas acima de cada barra
        for i, v in enumerate(quantidades):
            plt.text(i, v + 0.1, str(v), ha='center')

        # Exibe o gráfico em uma janela do sistema
        plt.show()

# ...


    def exibir_grafico_vendas_por_hora(self, vendas_por_hora):
        horas = list(vendas_por_hora.keys())
        quantidades = list(vendas_por_hora.values())

        plt.figure(figsize=(8, 6))
        plt.bar(horas, quantidades, color='blue')
        plt.xlabel('Horas')
        plt.ylabel('Quantidade de Vendas')
        plt.title('Quantidade de Vendas por Hora')
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Crie uma nova janela para exibir o gráfico
        grafico_window = tk.Toplevel(self.root)
        grafico_window.title("Gráfico de Vendas por Hora")
        grafico_window.geometry("800x600")

        # Crie um widget FigureCanvasTkAgg para exibir o gráfico na janela
        canvas = FigureCanvasTkAgg(plt.gcf(), master=grafico_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = Administracao(root)
    root.mainloop()
