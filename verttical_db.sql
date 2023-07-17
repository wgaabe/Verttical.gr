-- Criação da tabela Produtos
CREATE TABLE IF NOT EXISTS Produtos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nome TEXT NOT NULL,
    Valor REAL NOT NULL,
    Quantidade INTEGER NOT NULL,
    DataEntrada TEXT NOT NULL,
    HoraEntrada TEXT NOT NULL
);

-- Criação da tabela Vendas
CREATE TABLE IF NOT EXISTS Vendas (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Data TEXT NOT NULL,
    Hora TEXT NOT NULL,
    Produto TEXT NOT NULL,
    Quantidade INTEGER NOT NULL,
    ValorTotal REAL NOT NULL,
    PeriodoID INTEGER NOT NULL,
    FOREIGN KEY (PeriodoID) REFERENCES Periodos(ID)
);

-- Criação da tabela Periodos
CREATE TABLE IF NOT EXISTS Periodos (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    DataInicio TEXT NOT NULL,
    HoraInicio TEXT NOT NULL,
    DataFim TEXT,
    HoraFim TEXT
);