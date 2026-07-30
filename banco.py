# banco.py — Conexão e operações com banco de dados SQLite

def criar_banco():
    pass

def salvar_usuario(nome, senha):
    pass

def buscar_usuario(nome, senha):
    pass

def salvar_lote(dados_lote):
    pass

def buscar_historico(usuario_id):
    pass


if __name__ == "__main__":
    criar_banco()
    # Exemplo de uso das funções
    salvar_usuario("usuario1", "senha123")
    usuario = buscar_usuario("usuario1", "senha123")
    print(usuario)