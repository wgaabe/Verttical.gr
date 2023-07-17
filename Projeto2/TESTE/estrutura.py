import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import Calendar
from tkinter import ttk
from produto import Produto
from database import Database

class Estrutura:
    def __init__(self, interface):
        self.interface = interface
        self.produtos = Produto(self.interface)
        self.database = Database()

    def showload_status_periodo(self):
        periodo_aberto = self.database.obter_periodo_aberto()
    
        if periodo_aberto:
            periodo_id = periodo_aberto[0]
            produtos = self.database.obter_produtos_periodo(periodo_id)
            data_inicio = periodo_aberto[1]
            hora_inicio = periodo_aberto[2]
            status_periodo = f"Período Aberto - Início: {data_inicio} {hora_inicio}"
        else:
            produtos = []
            status_periodo = "Não existem períodos abertos"

            self.interface.lista_produtos.delete(0, tk.END)
            
        if produtos:
            for produto in produtos:
                nome = produto[1]
                valor = produto[2]
                quantidade = produto[3]
                produto_formatado = f"Nome: {nome}, Valor: {valor}, Quantidade: {quantidade}"
                self.interface.lista_produtos.insert(tk.END, produto_formatado)
        
        self.interface.status_periodo_label.config(text=status_periodo)
        

    def verificar_periodo_aberto(self):
        return self.database.obter_periodo_aberto()

    def iniciar_periodo(self):
        periodo_aberto = self.database.obter_periodo_aberto()
        if periodo_aberto:
            messagebox.showwarning("Período em Aberto", "Já existe um período em aberto. Finalize o período atual antes de criar um novo.")
        else:
            opcao = messagebox.askquestion("Iniciar Período", "Deseja iniciar o período na data e hora atual?")
            if opcao == 'yes':
                data_inicio = datetime.now().strftime("%d-%m-%Y")
                hora_inicio = datetime.now().strftime("%H:%M:%S")
                self.database.inserir_periodo(data_inicio, hora_inicio)
                messagebox.showinfo("Período Iniciado", "O período foi iniciado com sucesso!")
                self.produtos.exibir_produtos()
                self.showload_status_periodo()  # Atualizar status do período na interface
            else:
                self.abrir_janela_data_hora_manual(True)

    def finalizar_periodo(self):
        periodo_aberto = self.database.obter_periodo_aberto()
        if not periodo_aberto:
            messagebox.showwarning("Período não Iniciado", "Não há período em aberto para finalizar.")
        else:
            opcao = messagebox.askquestion("Finalizar Período", "Deseja finalizar o período na data e hora atual?")
            if opcao == 'yes':
                data_final = datetime.now().strftime("%d-%m-%Y")
                hora_final = datetime.now().strftime("%H:%M:%S")
                self.database.atualizar_periodo(periodo_aberto[0], data_final, hora_final)
                messagebox.showinfo("Período Finalizado", "O período foi finalizado com sucesso!")
                self.interface.lista_produtos.delete(0, tk.END)  # Limpar lista de produtos
                self.produtos.exibir_produtos()  # Carregar novos dados de produtos
                self.showload_status_periodo()  # Atualizar status do período na interface
            else:
                self.abrir_janela_data_hora_manual(False)

    def abrir_janela_data_hora_manual(self, iniciar):
        janela = tk.Toplevel()
        janela.title("Data e Hora Manual")
        
        # Calendário para selecionar a data
        calendario = Calendar(janela, selectmode="day", date_pattern="dd/mm/yyyy")
        calendario.pack(padx=10, pady=10)
        
        # Spinbox para inserir a hora manualmente
        lbl_hora = tk.Label(janela, text="Hora:")
        lbl_hora.pack(padx=10, pady=5)
        spin_hora = ttk.Spinbox(janela, from_=0, to=23, format="%02.0f")
        spin_hora.pack(padx=10, pady=5)
        
        # Spinbox para inserir o minuto manualmente
        lbl_minuto = tk.Label(janela, text="Minuto:")
        lbl_minuto.pack(padx=10, pady=5)
        spin_minuto = ttk.Spinbox(janela, from_=0, to=59, format="%02.0f")
        spin_minuto.pack(padx=10, pady=5)
        
        # Spinbox para inserir o segundo manualmente
        lbl_segundo = tk.Label(janela, text="Segundo:")
        lbl_segundo.pack(padx=10, pady=5)
        spin_segundo = ttk.Spinbox(janela, from_=0, to=59, format="%02.0f")
        spin_segundo.pack(padx=10, pady=5)
        
        # Botão para confirmar a seleção da data e hora
        btn_confirmar = tk.Button(janela, text="Confirmar", command=lambda: self.obter_data_hora(calendario, spin_hora, spin_minuto, spin_segundo, janela, iniciar))
        btn_confirmar.pack(padx=10, pady=10)

    def obter_data_hora(self, calendario, spin_hora, spin_minuto, spin_segundo, janela, iniciar):
        data_selecionada = calendario.selection_get()
        hora_selecionada = spin_hora.get()
        minuto_selecionado = spin_minuto.get()
        segundo_selecionado = spin_segundo.get()

        data = data_selecionada.strftime("%d-%m-%Y")
        hora = f"{hora_selecionada}:{minuto_selecionado}:{segundo_selecionado}"
        print(hora)

        if iniciar:
            self.database.inserir_periodo(data, hora)
            messagebox.showinfo("Período Iniciado", "O período foi iniciado com sucesso!")
        else:
            periodo_aberto = self.database.obter_periodo_aberto()
            if periodo_aberto:
                periodo_id = periodo_aberto[0]
                self.database.atualizar_periodo(periodo_id, data, hora)
                messagebox.showinfo("Período Finalizado", "O período foi finalizado com sucesso!")
            else:
                messagebox.showwarning("Período não Iniciado", "Não há período em aberto para finalizar.")

        janela.destroy()

    def registrar_venda(self):
        messagebox.showinfo("Aviso", "Venda registrada.")
