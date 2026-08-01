#Alan

# Cálculos de peso e carcaça
def calcular_peso_carcaca(peso_vivo, rendimento_percentual):
    peso_carcaca = peso_vivo * (rendimento_percentual / 100)
    return peso_carcaca

def calcular_arrobas(peso_carcaca):
    arrobas = peso_carcaca / 15
    return arrobas

def calcular_perda_transporte(peso_vivo, horas_totais):
    taxa_perda_hora = 0.005 #O valor da taxa de perda por hora não se tem um valor exato, pois vária de acordo com vários outros fatores, então pesquisei e coloquei um valor padrão fixo.
    perda_transporte = peso_vivo * taxa_perda_hora * horas_totais
    return perda_transporte

def estimar_peso_final(peso_inicial, gmd, dias):
    peso_final = peso_inicial + (gmd * dias)
    return peso_final

# Cálculos financeiros
def calcular_receita_bruta(arrobas, preco_arroba):
    pass

def calcular_receita_liquida(receita_bruta, total_impostos):
    pass

def calcular_lucro_liquido(receita_liquida, gastos_totais):
    pass

def calcular_ponto_equilibrio(gastos_totais, total_arrobas):
    pass

def calcular_lucro_por_cabeca(lucro_liquido, qtd_animais):
    pass

# Gastos de criação
def registrar_gasto_alimentacao(qtd_animais, dias, custo_diario):
    pass

def registrar_vacinas_obrigatorias(qtd_animais):
    pass

def registrar_medicamentos_opcionais(descricao, valor):
    pass

def registrar_frete(valor):
    pass

def registrar_mao_de_obra(valor):
    pass

def registrar_documentacao(custo_gta, outros):
    pass

def calcular_total_gastos(lista_gastos):
    pass





# Cauê

# Impostos
def calcular_funrural(receita_bruta, tipo_produtor):
    pass

def calcular_senar(receita_bruta):
    pass

def calcular_icms(receita_bruta, mesmo_estado, aliquota):
    pass

def calcular_total_impostos(receita_bruta, tipo_produtor, mesmo_estado, aliquota_icms):
    pass

def calcular_custo_total(custo_compra, gastos_criacao):
    pass

# Lote
def cadastrar_lote(raca, categoria, quantidade, peso_compra, preco_compra):
    pass

def registrar_refugo(qtd_refugo, valor_refugo):
    pass

def estimar_resultado_lote(lote, dias):
    pass

# Relatório
def exibir_resumo_lote(dados):
    pass

def exibir_resultado_financeiro(dados):
    pass

def exibir_alerta_lucro(lucro, ponto_equilibrio):
    pass

# Histórico — integra com banco.py
def salvar_resultado(dados_lote):
    pass

def consultar_historico(usuario_id):
    pass

# Autenticação — integra com banco.py
def cadastrar_usuario(nome, senha):
    pass

def fazer_login(nome, senha):
    pass