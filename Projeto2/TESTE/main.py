'''
from interface import Interface
from database import Database
from produto import Produto

def main():
    # Criar a instância do banco de dados
    database = Database()
    
    # Criar a instância de Produto
    produtos = Produto(interface)

    
    # Verificar se há um período em aberto
    periodo_aberto = database.obter_periodo_aberto()
    
    if periodo_aberto:
        periodo_id = periodo_aberto[0]
        produtos.exibir_produtos(periodo_id)
    
    # Criar a instância da interface com os parâmetros necessários
    interface = Interface(database, produtos)
    
    # Iniciar o loop principal da interface
    interface.executar()

if __name__ == "__main__":
    main()
'''