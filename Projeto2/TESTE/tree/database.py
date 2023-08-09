import sqlite3
import threading
import traceback

class Database:
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

    def criar_database(self):
        try:
            self.abrir_conexao()
            self.criar_tabela_produtos()
            self.criar_tabela_vendas()
            self.criar_tabela_periodos()
        except Exception as e:
            print("Erro ao criar o banco de dados:")
            print(traceback.format_exc())

    def inserir_periodo(self, data, hora):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute("INSERT INTO Periodos (DataInicio, HoraInicio) VALUES (?, ?)", (data, hora))
            except Exception as e:
                print("Erro ao inserir período:")
                print(traceback.format_exc())

    def atualizar_periodo(self, periodo_id, data_fim, hora_fim):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute("UPDATE Periodos SET DataFim = ?, HoraFim = ? WHERE ID = ?", (data_fim, hora_fim, periodo_id))
            except Exception as e:
                print("Erro ao atualizar período:")
                print(traceback.format_exc())

    def obter_periodo_aberto(self):
        try:
            self.abrir_conexao()
            with self.conexao:
                self.cursor.execute("SELECT ID, DataInicio, HoraInicio FROM Periodos WHERE DataFim IS NULL")
                periodo = self.cursor.fetchone()
                return periodo if periodo else ()
        except Exception as e:
            print("Erro ao obter período aberto:")
            print(traceback.format_exc())
            return None

    def excluir_produto(self, produto_id):
        with self.lock:
            try:
                self.abrir_conexao()
                self.cursor.execute("DELETE FROM Produtos WHERE ID = ?", (produto_id,))
                self.conexao.commit()
            except Exception as e:
                print("Erro ao excluir produto:")
                print(traceback.format_exc())
            finally:
                self.fechar_conexao()
    
    def inserir_produto(self, nome, valor, quantidade, data_entrada, hora_entrada, periodo_id):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute("INSERT INTO Produtos (Nome, Valor, Quantidade, DataEntrada, HoraEntrada, PeriodoID) VALUES (?, ?, ?, ?, ?, ?)",
                                        (nome, valor, quantidade, data_entrada, hora_entrada, periodo_id))
            except Exception as e:
                print("Erro ao inserir produto:")
                print(traceback.format_exc())

    def inserir_produto(self, nome, valor, quantidade, data_entrada, hora_entrada, periodo_id):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute("INSERT INTO Produtos (Nome, Valor, Quantidade, DataEntrada, HoraEntrada, PeriodoID) VALUES (?, ?, ?, ?, ?, ?)",
                                        (nome, valor, quantidade, data_entrada, hora_entrada, periodo_id))
            except Exception as e:
                print("Erro ao inserir produto:")
                print(traceback.format_exc())

    def obter_estoque_disponivel(self, nome_produto, periodo_id):
        produto_id = self.obter_id_produto(nome_produto, periodo_id)
        if produto_id:
            query = "SELECT quantidade FROM produtos WHERE id = ?"
            self.cursor.execute(query, (produto_id,))
            resultado = self.cursor.fetchone()
            if resultado:
                estoque_disponivel = resultado[0]
                return estoque_disponivel
        return None            

    def obter_produtos_periodo(self, periodo_id):
        with self.lock:
            try:
                self.abrir_conexao()
                self.cursor.execute(
                    "SELECT * FROM Produtos "
                    "WHERE PeriodoID = ? "
                    "AND ("
                    "   DataEntrada > (SELECT DataInicio FROM Periodos WHERE ID = ?) "
                    "   OR ("
                    "       DataEntrada = (SELECT DataInicio FROM Periodos WHERE ID = ?) "
                    "       AND HoraEntrada >= (SELECT HoraInicio FROM Periodos WHERE ID = ?) "
                    "   )"
                    ") "
                    "AND ("
                    "   DataEntrada < IFNULL((SELECT DataFim FROM Periodos WHERE ID = ?), DATE('now')) "
                    "   OR ("
                    "       DataEntrada = IFNULL((SELECT DataFim FROM Periodos WHERE ID = ?), DATE('now')) "
                    "       AND HoraEntrada <= IFNULL((SELECT HoraFim FROM Periodos WHERE ID = ?), TIME('now')) "
                    "   )"
                    ")",
                    (periodo_id, periodo_id, periodo_id, periodo_id, periodo_id, periodo_id, periodo_id)
                )
                produtos = self.cursor.fetchall()
                return produtos
            except Exception as e:
                print("Erro ao obter produtos do período:")
                print(traceback.format_exc())
                return []  # Retorna uma lista vazia em caso de erro
            
    def obter_id_produto(self, nome_produto, periodo_id):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute("SELECT ID FROM Produtos WHERE Nome = ? AND PeriodoID = ?", (nome_produto, periodo_id))
                    resultado = self.cursor.fetchone()
                    if resultado:
                        return resultado[0]
                    return None
            except Exception as e:
                print("Erro ao obter ID do produto:")
                print(traceback.format_exc())
                return None
            
    def obter_estoque_disponivel(self, produto_id, periodo_id):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute("SELECT Quantidade FROM Produtos WHERE ID = ? AND PeriodoID = ?", (produto_id, periodo_id))
                    resultado = self.cursor.fetchone()
                    if resultado:
                        return resultado[0]
                    return None
            except Exception as e:
                print("Erro ao obter estoque disponível do produto:")
                print(traceback.format_exc())
                return None

    def atualizar_estoque_produto(self, produto_id, nova_quantidade_estoque):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute(
                        "UPDATE Produtos SET Quantidade = ? WHERE ID = ?",
                        (nova_quantidade_estoque, produto_id)
                    )
            except Exception as e:
                print("Erro ao atualizar estoque do produto:")
                print(traceback.format_exc())

    def verificar_produto_periodo(self, produto_id, data_entrada, hora_entrada):
        self.abrir_conexao()
        with self.conexao:
            self.cursor.execute("SELECT COUNT(*) FROM Produtos WHERE ID = ? AND DataEntrada >= ? AND HoraEntrada >= ?", (produto_id, data_entrada, hora_entrada))
            resultado = self.cursor.fetchone()
            if resultado and resultado[0] > 0:
                return True
        return False
                
    def atualizar_produto(self, produto_id, nome, valor, quantidade):
        with self.lock:
            try:
                print("Produto ID:", produto_id)
                print("Nome:", nome)
                print("Valor:", valor)
                print("Quantidade:", quantidade)

                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute("UPDATE Produtos SET Nome = ?, Valor = ?, Quantidade = ? WHERE ID = ?",
                                        (nome, valor, quantidade, produto_id))
            except Exception as e:
                print("Erro ao atualizar produto:")
                print(traceback.format_exc())
            
    def registrar_venda(self, data_hora, produto, quantidade, valor_total, periodo_id, produto_id, venda_cortesia):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute(
                        "INSERT INTO vendas (data_hora, produto, quantidade, valor_total, periodo_id, produto_id, venda_cortesia) "
                        "VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (data_hora, produto, quantidade, valor_total, periodo_id, produto_id, venda_cortesia)
                    )
            except Exception as e:
                print("Erro ao registrar venda:")
                print(traceback.format_exc())

    def obter_dados_completos_produto_por_periodo(self, produto, periodo_id):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute(
                        "SELECT Nome, Valor, Quantidade, DataEntrada, HoraEntrada "
                        "FROM Produtos "
                        "WHERE Nome = ? AND PeriodoID = ?",
                        (produto, periodo_id)
                    )
                    resultado = self.cursor.fetchone()
                    if resultado:
                        return resultado
                    else:
                        return None
            except Exception as e:
                print("Erro ao obter dados completos do produto por período:")
                print(traceback.format_exc())
                return None
    def obter_quantidade_estoque(self, produto_id):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute("SELECT Quantidade FROM Produtos WHERE ID = ?", (produto_id,))
                    quantidade_estoque = self.cursor.fetchone()
                    if quantidade_estoque:
                        return quantidade_estoque[0]
                    else:
                        return None
            except Exception as e:
                print("Erro ao obter quantidade de estoque:")
                print(traceback.format_exc())
                return None

    def obter_quantidade_produto(self, produto_id):
        self.abrir_conexao()
        with self.conexao:
            self.cursor.execute("SELECT quantidade FROM produtos WHERE id = ?", (produto_id,))
            quantidade = self.cursor.fetchone()
            return quantidade[0] if quantidade else 0

   
    def obter_dados_completos_produto(self, produto_id):
        self.abrir_conexao()
        with self.conexao:
            self.cursor.execute("SELECT Nome, Valor, Quantidade, DataEntrada, HoraEntrada FROM Produtos WHERE ID = ?", (produto_id,))
            resultado = self.cursor.fetchone()
            if resultado:
                return resultado
            else:
                return None

    def inserir_venda(self,data_venda, hora_venda, total_venda, periodo_id, tipo_pagamento):
        with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute(
                        "INSERT INTO vendas (data_venda, hora_venda, total_venda, periodo_id, tipo_pagamento_id) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (data_venda, hora_venda, total_venda, periodo_id, tipo_pagamento)
                    )
                    venda_id = self.cursor.lastrowid
                    return venda_id
            except Exception as e:
                print("Erro ao registrar venda:")
                print(traceback.format_exc())
                return None  # Ou algum valor que indique um erro, se necessário

    def inserir_produto_itens_venda(self, venda_id, produto_id, quantidade, valor_unitario,valor_total_produto, venda_cortesia):
         with self.lock:
            try:
                self.abrir_conexao()
                with self.conexao:
                    self.cursor.execute(
                        "INSERT INTO itens_venda (venda_id, produto_id, quantidade_venda, valor_unitario, valor_total_produto, venda_cortesia) "
                        "VALUES (?, ?, ?, ?, ?, ?)",
                        (venda_id, produto_id, quantidade, valor_unitario, valor_total_produto, venda_cortesia)
                    )
                    venda_id = self.cursor.lastrowid
                    return venda_id
            except Exception as e:
                print("Erro ao registrar venda:")
                print(traceback.format_exc())
                return None  # Ou algum valor que indique um erro, se necessário

    def obter_valor_produto(self, produto, periodo_id):
        self.abrir_conexao()
        with self.conexao:
            self.cursor.execute(
                "SELECT valor FROM produtos WHERE nome = ? AND periodo_id = ?",
                (produto, periodo_id)
            )
            valor = self.cursor.fetchone()
            return valor[0] if valor else None

            
