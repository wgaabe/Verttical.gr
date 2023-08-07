CREATE TABLE "Periodos" (
	"ID"	INTEGER,
	"DataInicio"	TEXT NOT NULL,
	"HoraInicio"	TEXT NOT NULL,
	"DataFim"	TEXT,
	"HoraFim"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT)
)
CREATE TABLE Produtos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Valor REAL NOT NULL,
    Quantidade INTEGER NOT NULL,
    DataEntrada TEXT NOT NULL,
    HoraEntrada TEXT NOT NULL,
    PeriodoID INTEGER,
    FOREIGN KEY (PeriodoID) REFERENCES Periodos(ID)
)
CREATE TABLE vendas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_hora DATETIME,
    produto VARCHAR(100),
    quantidade INT,
    valor_total DECIMAL(10, 2),
    periodo_id INT,
    produto_id INT,
    venda_cortesia BOOLEAN,
    FOREIGN KEY (periodo_id) REFERENCES periodo(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);