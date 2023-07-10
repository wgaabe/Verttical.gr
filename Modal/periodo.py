from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import database

def abrir_janela_periodo_manual():
    janela = Toplevel()
    janela.title("Informar Data e Hora Manualmente")

    # Função para salvar a data e hora
    def salvar_data_hora():
        data = data_entry.get()
        hora = f"{hora_spinbox.get()}:{minuto_spinbox.get()}:{segundo_spinbox.get()}"
        if data and hora:
            # Restante do código para salvar a data e hora
            print(f"Data: {data}, Hora: {hora}")
            janela.destroy()
        else:
            messagebox.showwarning("Dados Inválidos", "Preencha todos os campos!")

    # Entry - Data
    Label(janela, text="Data:").grid(row=0, column=0, padx=10, pady=10)
    data_entry = DateEntry(janela, width=12, date_pattern='dd-mm-yyyy')
    data_entry.grid(row=0, column=1, padx=10, pady=10)

    # Entry - Hora
    Label(janela, text="Hora:").grid(row=2, column=0, padx=10, pady=10)
    #Hora
    hora_spinbox = Spinbox(janela, from_=0, to=23, width=2, wrap=True)
    hora_spinbox.grid(row=2, column=2, padx=20, pady=10)
    #MIN
    Label(janela, text=":").grid(row=2, column=3)
    minuto_spinbox = Spinbox(janela, from_=0, to=59, width=2, wrap=True)
    minuto_spinbox.grid(row=2, column=4, padx=2, pady=10)
    #SEG
    Label(janela, text=":").grid(row=2, column=5)
    segundo_spinbox = Spinbox(janela, from_=0, to=59, width=2, wrap=True)
    segundo_spinbox.grid(row=2, column=6, padx=2, pady=10)

    # Botão para confirmar
    Button(janela, text="Confirmar", command=salvar_data_hora).grid(row=3, column=1, columnspan=2, padx=10, pady=10)
