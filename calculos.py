import banco as banco_db
from dados import *
from banco import *

# Cálculos de peso e carcaça
def calcular_peso_carcaca(peso_vivo, rendimento_percentual):
    peso_carcaca = peso_vivo * (rendimento_percentual / 100)
    return peso_carcaca

def calcular_arrobas(peso_carcaca):
    arrobas = peso_carcaca / 15
    return arrobas

def estimar_peso_final(peso_inicial, gmd, dias):
    peso_final = peso_inicial + (gmd * dias)
    return peso_final

# Cálculos financeiros
def calcular_receita_bruta(arrobas, preco_arroba):
    return arrobas * preco_arroba

def calcular_receita_liquida(receita_bruta, total_impostos):
    return receita_bruta - total_impostos

def calcular_lucro_liquido(receita_liquida, gastos_totais):
    return receita_liquida - gastos_totais

def calcular_ponto_equilibrio(gastos_totais, total_arrobas):
    if total_arrobas <= 0:
        return 0
    return gastos_totais / total_arrobas

def calcular_lucro_por_cabeca(lucro_liquido, qtd_animais):
    if qtd_animais <= 0:
        return 0
    return lucro_liquido / qtd_animais

# Gastos de criação
def calcular_total_gastos(lista_gastos):
    if not lista_gastos:
        return 0
    return sum(lista_gastos)

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
    print("==========================================")

def exibir_estimativa(lote):
    estimativa = estimar_resultado_lote(lote, lote["dias_criacao"])
    print("\n===== ESTIMATIVA DO LOTE =====")
    print(f"Ganho médio diário estimado: {estimativa['gmd_medio']:.2f} kg/dia")
    print(f"Rendimento médio esperado:   {estimativa['rendimento_medio']*100:.1f}%")
    print(f"Peso final estimado:         {estimativa['peso_final_estimado']:.1f} kg por animal")
    print(f"Peso de carcaça estimado:    {estimativa['peso_carcaca_estimado']:.1f} kg por animal")
    print(f"Arrobas estimadas por animal:{estimativa['arrobas_estimadas']:.1f} @")
    print(f"Arrobas totais do lote:      {estimativa['arrobas_estimadas'] * lote['quantidade']:.1f} @")
    print("===============================")
    lote["peso_carcaca_estimado"] = estimativa["peso_carcaca_estimado"]

def exibir_alerta_lucro(lucro, ponto_equilibrio):
    print("\n========== ANÁLISE ==========")
    if lucro > ponto_equilibrio:
        print("LUCRO — operação foi positiva.")
    elif lucro < ponto_equilibrio:
        print("ATENÇÃO — operação com prejuízo.")
    else:
        print("NO LIMITE — sem lucro nem prejuízo.")
    print("==============================")

# Histórico
def salvar_resultado(dados_lote, usuario_id):
    return banco_db.salvar_resultado(dados_lote, usuario_id)

def consultar_historico(usuario_id):
    return banco_db.buscar_historico(usuario_id)

# Autenticação
def cadastrar_usuario(nome, email, senha):
    return salvar_usuario(nome, email, senha)

def fazer_login(email, senha):
    return buscar_usuario(email, senha)