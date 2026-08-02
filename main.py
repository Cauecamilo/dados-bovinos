from calculos import *
from dados import *
from banco import *

def iniciar_sistema():
    print("===========================================")
    print("  BEM-VINDO AO SISTEMA DE GESTÃO PECUÁRIA ")
    print("===========================================")

    # fazer_login() — aguardando banco.py

    opcao = ""
    while opcao != "3":
        opcao = menu_principal()

        if opcao == "1":
            lote = menu_lote()
            lista_gastos = menu_gastos()        # Alan vai retornar lista_gastos
            menu_venda(lote, lista_gastos)      # passa lista_gastos pro menu_venda

        elif opcao == "2":
            menu_historico()             # consultar_historico — aguardando banco.py

        elif opcao == "3":
            print("Encerrando o sistema. Até logo!")

        else:
            print("Opção inválida. Digite 1, 2 ou 3.")

def menu_principal():
    print("\n===== MENU PRINCIPAL =====")
    print("1. Cadastrar novo lote")
    print("2. Ver histórico")
    print("3. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_lote():
    print("\n===== CADASTRO DO LOTE =====")

    racas_validas = {raca.lower(): raca for raca in RACAS.keys()}
    raca = ""
    while True:
        print(f"Raças disponíveis: {', '.join(RACAS.keys())}")
        entrada_raca = input("Digite a raça: ").strip()
        raca = racas_validas.get(entrada_raca.lower())
        if raca is None:
            print("Raça inválida.")
        else:
            break

    categorias_validas = ["boi", "novilha", "vaca"]
    categoria = ""
    while categoria not in categorias_validas:
        categoria = input("Categoria (boi/novilha/vaca): ").lower().strip()
        if categoria not in categorias_validas:
            print("Categoria inválida.")

    quantidade = 0
    while quantidade <= 0:
        try:
            quantidade = int(input("Quantidade de animais: "))
            if quantidade <= 0:
                print("Digite um número maior que zero.")
        except:
            print("Digite apenas números inteiros.")

    peso_compra = 0
    while peso_compra < PESO_MINIMO:
        try:
            peso_compra = float(input("Peso médio de compra por animal (kg): "))
            if peso_compra < PESO_MINIMO:
                print(f"Digite um valor igual ou maior que {PESO_MINIMO} kg.")
        except:
            print("Digite apenas números.")

    preco_compra = 0
    while preco_compra < PRECO_MINIMO:
        try:
            preco_compra = float(input("Preço pago por animal (R$): "))
            if preco_compra < PRECO_MINIMO:
                print(f"Digite um valor maior ou igual a R$ {PRECO_MINIMO}.")
        except:
            print("Digite apenas números.")

    dias = 0
    while dias < CICLO_MINIMO_DIAS:
        try:
            dias = int(input("Tempo estimado de criação (dias): "))
            if dias < CICLO_MINIMO_DIAS:
                print(f"O ciclo mínimo é de {CICLO_MINIMO_DIAS} dias.")
        except:
            print("Digite apenas números inteiros.")

    lote = cadastrar_lote(raca, categoria, quantidade, peso_compra, preco_compra)
    lote["dias_criacao"] = dias

    # exibe estimativa
    estimativa = estimar_resultado_lote(lote, dias)
    print("\n===== ESTIMATIVA DO LOTE =====")
    print(f"Ganho médio diário estimado: {estimativa['gmd_medio']:.2f} kg/dia")
    print(f"Rendimento médio esperado:   {estimativa['rendimento_medio']*100:.1f}%")
    print(f"Peso final estimado:         {estimativa['peso_final_estimado']:.1f} kg por animal")
    print(f"Peso de carcaça estimado:    {estimativa['peso_carcaca_estimado']:.1f} kg por animal")
    print(f"Arrobas estimadas por animal:{estimativa['arrobas_estimadas']:.1f} @")
    print(f"Arrobas totais do lote:      {estimativa['arrobas_estimadas'] * quantidade:.1f} @")
    print("===============================")

    return lote

def menu_gastos():
    pass  # Alan

def menu_venda(lote, lista_gasto):
    print("\n===== DADOS DA VENDA =====")

    peso_venda = 0
    while peso_venda < PESO_MINIMO:
        try:
            peso_venda = float(input("Peso de venda do animal (kg): "))
            if peso_venda < PESO_MINIMO:
                print(f"Digite um valor igual ou maior que {PESO_MINIMO} kg.")
        except:
            print("Digite apenas números.")

    preco_arroba = 0
    while preco_arroba <= 0:
        try:
            preco_arroba = float(input("Preço da arroba na região (R$): "))
            if preco_arroba <= 0:
                print("Digite um valor maior que zero.")
        except:
            print("Digite apenas números.")

    opcoes_validas = ["PF", "PJ", "SE"]
    tipo_produtor = ""
    while tipo_produtor not in opcoes_validas:
        tipo_produtor = input("Tipo de produtor (PF/PJ/SE): ").upper()
        if tipo_produtor not in opcoes_validas:
            print("Opção inválida.")

    opcoes_estado = ["SIM", "NAO"]
    mesmo_estado = ""
    aliquota_icms = 0
    while mesmo_estado not in opcoes_estado:
        mesmo_estado = input("A venda é para dentro do mesmo estado? (SIM/NAO): ").upper()
        if mesmo_estado not in opcoes_estado:
            print("Digite SIM ou NAO.")
    if mesmo_estado == "NAO":
        while aliquota_icms <= 0:
            try:
                aliquota_icms = float(input("Alíquota do ICMS do seu estado (%): "))
                if aliquota_icms <= 0:
                    print("Digite um valor maior que zero.")
            except:
                print("Digite apenas números.")

    dias_transporte = 0
    while dias_transporte <= 0:  # CORREÇÃO: adicionada validação
        try:
            dias_transporte = int(input("Dias de transporte até o frigorífico: "))
            if dias_transporte <= 0:
                print("Digite um número maior que zero.")
        except:
            print("Digite apenas números inteiros.")

    qtd_refugo = -1
    while qtd_refugo < 0:
        try:
            qtd_refugo = int(input("Quantidade de animais refugo (0 se nenhum): "))
            if qtd_refugo < 0:
                print("Digite 0 ou um número positivo.")
        except:
            print("Digite apenas números inteiros.")

    valor_refugo = 0
    if qtd_refugo > 0:
        while valor_refugo <= 0:
            try:
                valor_refugo = float(input("Valor recebido por cada animal refugo (R$): "))
                if valor_refugo <= 0:
                    print("Digite um valor maior que zero.")
            except:
                print("Digite apenas números.")

    total_refugo = registrar_refugo(qtd_refugo, valor_refugo)

    resultados = {
        # dados do lote
        "raca":               lote["raca"],
        "categoria":          lote["categoria"],
        "quantidade":         lote["quantidade"],
        "peso_compra":        lote["peso_compra"],
        "preco_compra":       lote["preco_compra"],
        "custo_compra_total": lote["custo_compra_total"],
        # dados da venda
        "peso_venda":         peso_venda,
        "preco_arroba":       preco_arroba,
        "dias_transporte":    dias_transporte,
        "qtd_refugo":         qtd_refugo,
        "valor_refugo":       valor_refugo,
        "total_refugo":       total_refugo,
        # resultados financeiros — Alan preenche
        "receita_bruta":      0,
        "total_impostos":     0,
        "receita_liquida":    0,
        "gastos_totais":      0,
        "custo_total":        0,
        "lucro_liquido":      0,
        "lucro_por_cabeca":   0,
        "ponto_equilibrio":   0,
    }

    exibir_resumo_lote(resultados)
    exibir_resultado_financeiro(resultados)
    exibir_alerta_lucro(resultados["lucro_liquido"], resultados["ponto_equilibrio"])
    salvar_resultado(resultados)

def menu_historico():
    # aguardando banco.py
    print("Histórico disponível em breve.")

iniciar_sistema()
