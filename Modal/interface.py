from tkinter import *
from tkinter import messagebox,Tk, Entry, StringVar
from datetime import datetime
import periodo  # Importar o módulo "periodo" para acessar suas funções
import database

def cadastrar_produto():
    janela = Toplevel()
    janela.title("Cadastro de Produto")

    # Função para salvar o produto no banco de dados
    def salvar_produto():
        nome = nome_entry.get()
        valor = valor_entry.get()
        quantidade = quantidade_entry.get()
        data_entrada = datetime.now().strftime("%Y-%m-%d")
        hora_entrada = datetime.now().strftime("%H:%M:%S")

        if nome and valor and quantidade and data_entrada and hora_entrada:
            # Chamar a função do arquivo database.py para inserir o produto no banco de dados
            database.inserir_produto(nome, valor, quantidade, data_entrada, hora_entrada)
            messagebox.showinfo("Cadastro de Produto", "Produto cadastrado com sucesso!")
            janela.destroy()

            exibir_produtos()
        else:
            messagebox.showwarning("Dados Inválidos", "Preencha todos os campos!")

    # Labels e Entry
    Label(janela, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
    nome_entry = Entry(janela)
    nome_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(janela, text="Valor:").grid(row=1, column=0, padx=10, pady=10)
    valor_entry = Entry(janela)
    valor_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(janela, text="Quantidade:").grid(row=2, column=0, padx=10, pady=10)
    quantidade_entry = Entry(janela)
    quantidade_entry.grid(row=2, column=1, padx=10, pady=10)

    # Botão para confirmar o cadastro do produto
    Button(janela, text="Cadastrar", command=salvar_produto).grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def iniciar_periodo():
    opcao = messagebox.askquestion("Iniciar Período", "Deseja iniciar o período na data e hora atual?")

    if opcao == 'yes':
        data_inicio = datetime.now().strftime("%d-%m-%Y")
        hora_inicio = datetime.now().strftime("%H:%M:%S")

        periodo_aberto = database.verificar_periodo_aberto()
        if periodo_aberto:
            messagebox.showwarning("Período em Andamento", "Existe um período em andamento. Finalize-o antes de iniciar um novo período.")
        else:
            database.inserir_periodo(data_inicio, hora_inicio)
            messagebox.showinfo("Período Iniciado", "O período foi iniciado com sucesso!")
    else:
        periodo.abrir_janela_periodo_manual()  # Chame a função "abrir_janela_periodo_manual" do arquivo "periodo.py"


def finalizar_periodo():
    opcao = messagebox.askquestion("Finalizar Período", "Deseja finalizar o período na data e hora atual?")

    if opcao == 'yes':
        data_fim = datetime.now().strftime("%d-%m-%Y")
        hora_fim = datetime.now().strftime("%H:%M:%S")

        periodo_id = database.obter_ultimo_periodo_aberto()
        if periodo_id:
            database.atualizar_periodo(periodo_id, data_fim, hora_fim)
            messagebox.showinfo("Período Finalizado", "O período foi finalizado com sucesso!")
        else:
            messagebox.showwarning("Nenhum Período Aberto", "Não há nenhum período aberto para finalizar.")
    else:
        periodo.abrir_janela_periodo_manual()  # Chame a função "abrir_janela_periodo_manual" do arquivo "periodo.py"


def exibir_produtos():
    listbox.delete(0, END)  # Limpar a lista antes de preenchê-la novamente

    data_inicio, hora_inicio = database.obter_periodo_iniciado()
    if data_inicio and hora_inicio:
        produtos = database.obter_produtos_periodo_iniciado(data_inicio, hora_inicio)
        for produto in produtos:
            listbox.insert(END, f"Nome: {produto[1]} - Valor: {produto[2]} - Quantidade: {produto[3]}")


# Criação da janela principal
janela_principal = Tk()
janela_principal.title("Controle de Vendas")

# Botões de Iniciar Período e Finalizar Período
Button(janela_principal, text="Iniciar Período", command=iniciar_periodo).grid(row=0, column=0, padx=10, pady=10)
Button(janela_principal, text="Finalizar Período", command=finalizar_periodo).grid(row=0, column=1, padx=10, pady=10)

# Botões de cadastrode produto
Button(janela_principal, text="Cadastrar Produto", command=cadastrar_produto).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Criação do componente Listbox para exibir a lista de produtos
listbox = Listbox(janela_principal, width=50)
listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Inicia a interface
janela_principal.mainloop()

def exibir_menu():
    # Código para exibir o menu principal da interface
    pass

def obter_dados_input():
    # Código para obter os dados inseridos pelo usuário na interface
    pass

def exibir_resultados(dados):
    # Código para exibir os resultados na interface
    pass