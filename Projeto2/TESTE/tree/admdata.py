import sqlite3
import threading
import traceback

#pip install matplotlib

class admdata:
    def __init__(self):
        self.conexao = None
        self.cursor = None
        self.lock = threading.Lock()

    def conectar(self, nome_banco):
        self.conexao = sqlite3.connect(nome_banco)
        self.cursor = self.conexao.cursor()

    def abrir_conexao(self):
        self.conectar('base/banco.db')

    def fechar_conexao(self):
        if self.cursor:
            self.cursor.close()
        if self.conexao:
            self.conexao.close()

    def obter_periodos(self):
        try:
            self.abrir_conexao()
            with self.conexao:
                query = "SELECT * FROM Periodos"
                self.cursor.execute(query)
                periodos = self.cursor.fetchall()
                return periodos
        except sqlite3.Error as e:
            print("Erro ao obter períodos:", e)
        finally:
            self.fechar_conexao()

    """        
    def obter_periodos_entre_datas2(self, data_inicio_formatada, data_fim_formatada):
        try:
            self.abrir_conexao()
            with self.conexao:
                print("Data Início:", data_inicio_formatada)
                print("Data Fim:", data_fim_formatada)
                query = "SELECT * FROM Periodos WHERE DataInicio BETWEEN ? AND ?"
                self.cursor.execute(query, (data_inicio_formatada, data_fim_formatada))
                periodos = self.cursor.fetchall()
                return periodos
        except sqlite3.Error as e:
            print("Erro ao obter períodos entre datas:", e)
        finally:
            self.fechar_conexao()
    """
    
    def obter_periodos_entre_datas(self, data_inicio, data_fim):
        try:
            self.abrir_conexao()
            with self.conexao:
                print("Data Início:", data_inicio)
                print("Data Fim:", data_fim)
                query = "SELECT * FROM Periodos WHERE DataInicio BETWEEN ? AND ?"
                self.cursor.execute(query, (data_inicio, data_fim))
                periodos = self.cursor.fetchall()
                return periodos
        except sqlite3.Error as e:
            print("Erro ao obter períodos entre datas:", e)
        finally:
            self.fechar_conexao()       

    def obter_vendas_por_periodo(self, periodo_id):
        try:
            self.abrir_conexao()
            with self.conexao:
                query = "SELECT * FROM vendas WHERE periodo_id = ?"
                self.cursor.execute(query, (periodo_id,))
                vendas = self.cursor.fetchall()
                return vendas
        except sqlite3.Error as e:
            print("Erro ao obter vendas por período:", e)
        finally:
            self.fechar_conexao()

    def obter_quantidade_vendas_por_hora(self, periodo_id):
        try:
            self.abrir_conexao()
            with self.conexao:
                query = """
                SELECT strftime('%H', hora_venda) AS hora, COUNT(*) AS quantidade
                FROM vendas
                WHERE periodo_id = ?
                GROUP BY hora
                ORDER BY hora
                """
                self.cursor.execute(query, (periodo_id,))
                vendas_por_hora = self.cursor.fetchall()
                return {f"{hora}:00": quantidade for hora, quantidade in vendas_por_hora}
        except sqlite3.Error as e:
            print("Erro ao obter quantidade de vendas por hora:", e)
        finally:
            self.fechar_conexao()

    def cadastrar_metodo_pagamento(self, nome, taxa):
        try:
            self.abrir_conexao()
            with self.conexao:
                query = "INSERT INTO tipos_pagamentos (nome, taxa_banco) VALUES (?, ?)"
                self.cursor.execute(query, (nome, taxa))
                self.conexao.commit()
        except sqlite3.Error as e:
            print("Erro ao cadastrar método de pagamento:", e)
        finally:
            self.fechar_conexao()    
            