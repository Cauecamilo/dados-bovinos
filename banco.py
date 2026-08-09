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
    senha           TEXT NOT NULL,
    tipo_usuario    TEXT NOT NULL DEFAULT 'comum' CHECK (tipo_usuario IN ('admin', 'comum')),
    data_criacao    TEXT NOT NULL DEFAULT (datetime('now')))
""");
    


#ESSA TABELA SERVE PARA SALVARMOS OS RESULTADOS DE CADA LOTE, PARA QUE POSSAMOS TER UM HISTÓRICO DE CADA UM
    cursor.execute("""CREATE TABLE IF NOT EXISTS resultados_lote (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id          INTEGER NOT NULL,
    raca                TEXT,
    categoria           TEXT,
    quantidade          INTEGER,
    peso_compra         REAL,
    preco_compra        REAL,
    custo_compra_total  REAL,
    peso_venda          REAL,
    preco_arroba        REAL,
    dias_transporte     INTEGER,
    qtd_refugo          INTEGER,
    valor_refugo        REAL,
    total_refugo        REAL,
    receita_bruta       REAL,
    total_impostos      REAL,
    receita_liquida     REAL,
    gastos_totais       REAL,
    custo_total         REAL,
    lucro_liquido       REAL,
    lucro_por_cabeca    REAL,
    ponto_equilibrio    REAL,
    data_registro       TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id))""")

    cursor.execute("DROP TABLE IF EXISTS racas_bovinas;")

    conexao.commit()

    pass

def salvar_usuario(nome, email, senha):
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
            (nome, email, senha)
        )
        conexao.commit()
        print(f"Usuário {nome} cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Já existe um usuário cadastrado com esse email.")


def buscar_usuario(email, senha):
    cursor.execute(
        "SELECT id, nome, tipo_usuario FROM usuarios WHERE email = ? AND senha = ?",
        (email, senha)
    )
    usuario = cursor.fetchone()
    if usuario:
        print(f"Login bem-sucedido! Bem-vindo, {usuario[1]}.")
        return usuario
    else:
        print("Email ou senha incorretos.")
        return None

def salvar_resultado(resultados, usuario_id):
    cursor.execute("""
        INSERT INTO resultados_lote (
            usuario_id, raca, categoria, quantidade, peso_compra, preco_compra,
            custo_compra_total, peso_venda, preco_arroba, dias_transporte,
            qtd_refugo, valor_refugo, total_refugo, receita_bruta, total_impostos,
            receita_liquida, gastos_totais, custo_total, lucro_liquido,
            lucro_por_cabeca, ponto_equilibrio
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        usuario_id,
        resultados["raca"], resultados["categoria"], resultados["quantidade"],
        resultados["peso_compra"], resultados["preco_compra"], resultados["custo_compra_total"],
        resultados["peso_venda"], resultados["preco_arroba"], resultados["dias_transporte"],
        resultados["qtd_refugo"], resultados["valor_refugo"], resultados["total_refugo"],
        resultados["receita_bruta"], resultados["total_impostos"], resultados["receita_liquida"],
        resultados["gastos_totais"], resultados["custo_total"], resultados["lucro_liquido"],
        resultados["lucro_por_cabeca"], resultados["ponto_equilibrio"]
    ))
    conexao.commit()
    print("Resultado do lote salvo com sucesso no histórico!")

def buscar_historico(usuario_id):
    cursor.execute("""
        SELECT raca, categoria, quantidade, lucro_liquido, data_registro
        FROM resultados_lote
        WHERE usuario_id = ?
        ORDER BY data_registro DESC
    """, (usuario_id,))
    return cursor.fetchall()

criar_banco()