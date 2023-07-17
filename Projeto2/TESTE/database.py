import sqlite3
import threading

class Database:
    def __init__(self):
        self.conexao = None
        self.cursor = None
        self.lock = threading.Lock()

    def conectar(self, nome_banco):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()

    def abrir_conexao(self):
        self.conectar('banco.db')

    def fechar_conexao(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()    

    def criar_database(self):
        self.abrir_conexao()
        self.criar_tabela_produtos()
        self.criar_tabela_vendas()
        self.criar_tabela_periodos()

    def inserir_periodo(self, data, hora):
        self.abrir_conexao()
        with self.conexao:
            self.cursor.execute("INSERT INTO Periodos (DataInicio, HoraInicio) VALUES (?, ?)", (data, hora))

    def atualizar_periodo(self, periodo_id, data_fim, hora_fim):
        self.abrir_conexao()
        with self.conexao:
            self.cursor.execute("UPDATE Periodos SET DataFim = ?, HoraFim = ? WHERE ID = ?", (data_fim, hora_fim, periodo_id))

    def obter_periodo_aberto(self):
        self.abrir_conexao()
        with self.conexao:
            self.cursor.execute("SELECT * FROM Periodos WHERE DataFim IS NULL")
            periodo = self.cursor.fetchone()
            return periodo
    
    def inserir_produto(self, nome, valor, quantidade, data_entrada, hora_entrada):
        self.abrir_conexao()
        with self.conexao:
            self.cursor.execute("INSERT INTO Produtos (Nome, Valor, Quantidade, DataEntrada, HoraEntrada) VALUES (?, ?, ?, ?, ?)",
                                (nome, valor, quantidade, data_entrada, hora_entrada))

    def obter_produtos_periodo(self, periodo_id):
        self.abrir_conexao()
        try:
            self.cursor.execute(
                "SELECT * FROM Produtos "
                "WHERE DataEntrada >= (SELECT DataInicio FROM Periodos WHERE ID = ?) "
                "AND HoraEntrada >= (SELECT HoraInicio FROM Periodos WHERE ID = ?) "
                "AND (DataEntrada <= (SELECT DataFim FROM Periodos WHERE ID = ?) OR (SELECT DataFim FROM Periodos WHERE ID = ?) IS NULL) "
                "AND (HoraEntrada <= (SELECT HoraFim FROM Periodos WHERE ID = ?) OR (SELECT HoraFim FROM Periodos WHERE ID = ?) IS NULL)",
                (periodo_id, periodo_id, periodo_id, periodo_id, periodo_id, periodo_id)
            )
            produtos = self.cursor.fetchall()
            return produtos
        except sqlite3.Error as error:
            print("Erro ao executar a consulta SQL:", error)
        finally:
            self.fechar_conexao()


    def criar_tabela_produtos(self):
        self.abrir_conexao()
        with self.conexao:
            sql = """
            CREATE TABLE IF NOT EXISTS Produtos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Valor REAL NOT NULL,
                Quantidade INTEGER NOT NULL,
                DataEntrada TEXT NOT NULL,
                HoraEntrada TEXT NOT NULL
            )
            """
            self.cursor.execute(sql)

    def criar_tabela_vendas(self):
        self.abrir_conexao()
        with self.conexao:
            sql = """
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
            """
            self.cursor.execute(sql)

    def criar_tabela_periodos(self):
        self.abrir_conexao()
        with self.conexao:
            sql = """
            CREATE TABLE IF NOT EXISTS Periodos (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                DataInicio TEXT NOT NULL,
                HoraInicio TEXT NOT NULL,
                DataFim TEXT,
                HoraFim TEXT
            )
            """
            self.cursor.execute(sql)
