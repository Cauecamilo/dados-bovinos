# banco.py — Conexão e operações com banco de dados SQLite
import sqlite3

conexao = sqlite3.connect("banco.db")
cursor = conexao.cursor()


def criar_banco():

# ESSA TABELA É A DOS DADOS DO USUÁRIO
    cursor.execute ("""CREATE TABLE IF NOT EXISTS usuarios (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    senha_hash      TEXT NOT NULL,
    tipo_usuario    TEXT NOT NULL DEFAULT 'comum' CHECK (tipo_usuario IN ('admin', 'comum')),
    data_criacao    TEXT NOT NULL DEFAULT (datetime('now')))
""");
    

# ESSA TABELA SERVE PARA SABERMOS OS TIPOS DE RAÇAS EXISTENTES E O PERCENTUAL DE CADA UM
    cursor.execute (""" CREATE TABLE IF NOT EXISTS racas_bovinas (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                        TEXT NOT NULL UNIQUE,
    rendimento_carcaca_esperado REAL,
    observacoes                 TEXT)""");


# ESSA TABELA SERVE PARA ANOTARMOS OS TIPOS DE GASTOS
    cursor.execute ("""CREATE TABLE IF NOT EXISTS categorias_gasto (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    nome    TEXT NOT NULL UNIQUE)""")


# ESSA TABELA SERVE COMO UM REGISTRO GERAL DE CADA ANIMAL
    cursor.execute ("""CREATE TABLE IF NOT EXISTS animais (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    identificador           TEXT,
    raca_id                 INTEGER,
    tipo                    TEXT NOT NULL CHECK (tipo IN ('boi', 'novilha', 'vaca')),
    usuario_id              INTEGER NOT NULL,
    data_entrada            TEXT,
    status                  TEXT NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'vendido', 'morto')),
    tempo_estimado_criacao  INTEGER,
    FOREIGN KEY (raca_id) REFERENCES racas_bovinas (id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id))""")


#ESSA TABELA SERVE PARA A CRIAÇAO DE CADA LOTE
    cursor.execute ("""CREATE TABLE IF NOT EXISTS lotes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nome            TEXT,
    usuario_id      INTEGER NOT NULL,
    data_criacao    TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id))""")


#ESSA TABELA SERVE PARA OS DADOS DE COMPRA
    cursor.execute("""CREATE TABLE IF NOT EXISTS compras (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id       INTEGER,
    data            TEXT,
    peso_compra     REAL,
    valor_pago      REAL,
    fornecedor      TEXT,
    FOREIGN KEY (animal_id) REFERENCES animais (id))""")

#ESSA TABELA SERVE PARA SABERMOS OS DADOS DA VENDA DOS ANIMAIS
    cursor.execute ("""CREATE TABLE IF NOT EXISTS vendas (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id               INTEGER,
    data                     TEXT,
    peso_venda               REAL,
    valor_recebido           REAL,
    valor_arroba_na_venda    REAL,
    FOREIGN KEY (animal_id) REFERENCES animais (id))""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS dietas (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome                TEXT NOT NULL,
    descricao           TEXT,
    ganho_esperado_dia  REAL,
    fonte_cientifica    TEXT)""")

#ESSA TABELA SERVE PARA SABERMOS QUAL FOI O TIPO DE DIETA SEGUIDA POR CADA LOTE
    cursor.execute("""CREATE TABLE IF NOT EXISTS lote_dietas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    lote_id       INTEGER NOT NULL,
    dieta_id        INTEGER NOT NULL,
    data_inicio     TEXT,
    data_fim        TEXT,
    FOREIGN KEY (lote_id) REFERENCES lotes (id),
    FOREIGN KEY (dieta_id) REFERENCES dietas (id))""")

    conexao.commit()



    pass

def coletar_dados_login():
    pass
  
def salvar_usuario(nome, senha):
    pass

def buscar_usuario(nome, senha):
    pass

def salvar_lote(dados_lote):
    pass

def buscar_historico(usuario_id):
    pass


criar_banco()