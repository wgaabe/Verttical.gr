from admdata import admdata

class AdmController:
    def __init__(self, adm):
        self.adm = adm
        self.admdata = admdata()

    def carregar_metodos_pagamento(self):
        metodos_pagamento = self.admdata.obter_metodos_pagamento()
        self.adm.carregar_metodos_pagamento(metodos_pagamento)

    def cadastrar_metodo_pagamento(self, nome, taxa):
        try:
            self.admdata.cadastrar_metodo_pagamento(nome, taxa)
            self.carregar_metodos_pagamento()  # Atualiza a lista após o cadastro
        except Exception as e:
            # Trate a exceção ou mostre uma mensagem de erro para o usuário
            pass

    def excluir_metodo_pagamento(self, metodo_id):
        try:
            self.admdata.excluir_metodo_pagamento(metodo_id)
            self.carregar_metodos_pagamento()  # Atualiza a lista após a exclusão
        except Exception as e:
            # Trate a exceção ou mostre uma mensagem de erro para o usuário
            pass

    # Adicione outros métodos conforme necessário para interagir com a interface e a camada de dados
