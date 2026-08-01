from dados import *
from banco import *

# ── ALAN ──

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


# ── CAUÊ ──

# Impostos
def calcular_funrural(receita_bruta, tipo_produtor):
    if tipo_produtor == "PF":
        funrural = receita_bruta * FUNRURAL_PF
    elif tipo_produtor == "PJ":
        funrural = receita_bruta * FUNRURAL_PJ
    else:
        funrural = receita_bruta * FUNRURAL_SE
    return funrural

def calcular_senar(receita_bruta):
    senar = receita_bruta * SENAR
    return senar

def calcular_icms(receita_bruta, aliquota_icms):
    icms = receita_bruta * (aliquota_icms / 100)
    return icms

def calcular_total_impostos(receita_bruta, tipo_produtor, aliquota_icms):
    funrural = calcular_funrural(receita_bruta, tipo_produtor)
    senar    = calcular_senar(receita_bruta)
    icms     = calcular_icms(receita_bruta, aliquota_icms)
    return funrural + senar + icms

def calcular_custo_total(custo_compra, lista_gastos):
    gastos_criacao = calcular_total_gastos(lista_gastos)
    return custo_compra + gastos_criacao

# Lote
def cadastrar_lote(raca, categoria, quantidade, peso_compra, preco_compra):
    lote = {
        "raca": raca,
        "categoria": categoria,
        "quantidade": quantidade,
        "peso_compra": peso_compra,
        "preco_compra": preco_compra,
        "custo_compra_total": quantidade * preco_compra,
        "gmd_min": RACAS[raca]["gmd_min"],
        "gmd_max": RACAS[raca]["gmd_max"],
        "rendimento_min": RACAS[raca]["rendimento_min"],
        "rendimento_max": RACAS[raca]["rendimento_max"],
    }
    return lote

def registrar_refugo(qtd_refugo, valor_refugo):
    return qtd_refugo * valor_refugo

def estimar_resultado_lote(lote, dias):
    gmd_medio        = (lote["gmd_min"] + lote["gmd_max"]) / 2
    peso_final       = lote["peso_compra"] + (gmd_medio * dias)
    rendimento_medio = (lote["rendimento_min"] + lote["rendimento_max"]) / 2
    peso_carcaca     = peso_final * rendimento_medio
    arrobas          = peso_carcaca / 15
    return {
        "gmd_medio":             gmd_medio,
        "peso_final_estimado":   peso_final,
        "rendimento_medio":      rendimento_medio,
        "peso_carcaca_estimado": peso_carcaca,
        "arrobas_estimadas":     arrobas,
    }

# Relatório
def exibir_resumo_lote(resultados):
    print("\n========== RESUMO DO LOTE ==========")
    print(f"Raça:               {resultados['raca']}")
    print(f"Categoria:          {resultados['categoria']}")
    print(f"Quantidade:         {resultados['quantidade']} animais")
    print(f"Peso de compra:     {resultados['peso_compra']} kg por animal")
    print(f"Preço de compra:    R$ {resultados['preco_compra']:.2f} por animal")
    print(f"Custo total compra: R$ {resultados['custo_compra_total']:.2f}")
    print("=====================================")

def exibir_resultado_financeiro(resultados):
    print("\n========== RESULTADO FINANCEIRO ==========")
    print(f"Peso de venda:       {resultados['peso_venda']} kg")
    print(f"Preço da arroba:     R$ {resultados['preco_arroba']:.2f}")
    print(f"Receita bruta:       R$ {resultados['receita_bruta']:.2f}")
    print(f"Total de impostos:   R$ {resultados['total_impostos']:.2f}")
    print(f"Receita líquida:     R$ {resultados['receita_liquida']:.2f}")
    print(f"Gastos de criação:   R$ {resultados['gastos_totais']:.2f}")
    print(f"Custo total:         R$ {resultados['custo_total']:.2f}")
    print(f"Lucro líquido:       R$ {resultados['lucro_liquido']:.2f}")
    print(f"Lucro por cabeça:    R$ {resultados['lucro_por_cabeca']:.2f}")
    print(f"Ponto de equilíbrio: R$ {resultados['ponto_equilibrio']:.2f} por @")
    print(f"Animais refugo:      {resultados['qtd_refugo']} (R$ {resultados['total_refugo']:.2f})")
    print("==========================================")

def exibir_alerta_lucro(lucro, ponto_equilibrio):
    print("\n========== ANÁLISE ==========")
    if lucro > ponto_equilibrio:
        print("LUCRO — operação foi positiva.")
    elif lucro < ponto_equilibrio:
        print("ATENÇÃO — operação com prejuízo.")
    else:
        print("NO LIMITE — sem lucro nem prejuízo.")
    print("==============================")

# Histórico — aguardando banco.py
def salvar_resultado(dados_lote):
    pass

def consultar_historico(usuario_id):
    pass

# Autenticação — aguardando banco.py
def cadastrar_usuario(nome, senha):
    pass

def fazer_login(nome, senha):
    return True  # temporário até banco estar pronto