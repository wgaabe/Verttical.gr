import sqlite3

def conectar_banco():
    conn = sqlite3.connect('banco.db')
    # Configurações adicionais, se necessário
    return conn

def criar_tabela():
    conn = conectar_banco()
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Produtos (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Valor REAL NOT NULL,
            Quantidade INTEGER NOT NULL,
            DataEntrada TEXT NOT NULL,
            HoraEntrada TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vendas (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Data TEXT NOT NULL,
            Hora TEXT NOT NULL,
            Produto TEXT NOT NULL,
            Quantidade INTEGER NOT NULL,
            ValorTotal REAL NOT NULL,
            PeriodoID INTEGER NOT NULL,
            FOREIGN KEY (PeriodoID) REFERENCES Periodos(ID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Periodos (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            DataInicio TEXT NOT NULL,
            HoraInicio TEXT NOT NULL,
            DataFim TEXT,
            HoraFim TEXT
        )
    ''')

    conn.commit()
    conn.close()

def inserir_produto(nome, valor, quantidade, data_entrada, hora_entrada):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Produtos (Nome, Valor, Quantidade, DataEntrada, HoraEntrada) VALUES (?, ?, ?, ?, ?)",
                   (nome, valor, quantidade, data_entrada, hora_entrada))
    conn.commit()
    conn.close()


def inserir_dados(dados):
    conn = conectar_banco()
    cursor = conn.cursor()
    # Código para inserir dados na tabela
    conn.commit()
    conn.close()

def obter_dados():
    conn = conectar_banco()
    cursor = conn.cursor()
    # Código para obter dados da tabela
    conn.close()

def inserir_periodo(data, hora):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Periodos (DataInicio, HoraInicio) VALUES (?, ?)", (data, hora))
    conn.commit()
    conn.close()

def atualizar_periodo(periodo_id, data, hora):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("UPDATE Periodos SET DataFim = ?, HoraFim = ? WHERE ID = ?", (data, hora, periodo_id))
    conn.commit()
    conn.close()

def obter_ultimo_periodo_aberto():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT ID FROM Periodos WHERE DataFim IS NULL ORDER BY ID DESC LIMIT 1")
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return resultado[0]
    else:
        return None
    
def verificar_periodo_aberto():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT ID FROM Periodos WHERE DataFim IS NULL")
    resultado = cursor.fetchone()
    conn.close()

def obter_periodo_iniciado():
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT DataInicio, HoraInicio FROM Periodos WHERE DataFim IS NULL")
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        return resultado[0], resultado[1]
    else:
        return None, None

def obter_produtos_periodo_iniciado(data_inicio, hora_inicio):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute("SELECT Nome, Valor, Quantidade FROM Produtos WHERE DataEntrada = ? AND HoraEntrada = ?", (data_inicio, hora_inicio))
    produtos = cursor.fetchall()
    conn.close()

    return produtos






