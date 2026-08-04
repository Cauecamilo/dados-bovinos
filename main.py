import banco
from calculos import *
from dados import *
from banco import *

def iniciar_sistema():
    print("===========================================")
    print("  BEM-VINDO AO SISTEMA DE GESTÃO PECUÁRIA ")
    print("===========================================")

    usuario_id = fazer_login_ou_cadastro()

    opcao = ""
    while opcao != "3":
        opcao = menu_principal()

        if opcao == "1":
            lote = menu_lote()
            lista_gastos = menu_gastos()        # Alan vai retornar lista_gastos
            menu_venda(lote, lista_gastos, usuario_id)      # passa lista_gastos pro menu_venda

        elif opcao == "2":
            menu_historico(usuario_id)             # consultar_historico — aguardando banco.py

        elif opcao == "3":
            print("Encerrando o sistema. Até logo!")

        else:
            print("Opção inválida. Digite 1, 2 ou 3.")


def fazer_login_ou_cadastro():
    while True:
        print("\n1. Fazer login")
        print("2. Cadastrar novo usuário")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            email = input("Email: ")
            senha = input("Senha: ")
            usuario = banco.buscar_usuario(email, senha)
            tentativas = 1
            while usuario is None and tentativas < 3:
                email = input("Email: ")
                senha = input("Senha: ")
                usuario = banco.buscar_usuario(email, senha)
                tentativas += 1

            if usuario is None:
                print("Número máximo de tentativas excedido. Voltando ao menu...")
                continue

            return usuario[0]

        elif opcao == "2":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            banco.salvar_usuario(nome, email, senha)
            usuario = banco.buscar_usuario(email, senha)
            if usuario is None:
                print("Não foi possível concluir o cadastro.")
                continue
            return usuario[0]

        elif opcao == "3":
            print("Encerrando o sistema. Até logo!")
            exit()

        else:
            print("Opção inválida.")
            continue
    
def menu_principal():
    print("\n===== MENU PRINCIPAL =====")
    print("1. Cadastrar novo lote")
    print("2. Ver histórico")
    print("3. Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def menu_lote():
    print("\n===== CADASTRO DO LOTE =====")

    racas_validas = list(RACAS.keys())
    raca = ""
    while True:
        print(f"Raças disponíveis: {', '.join(racas_validas)}")
        raca_digitada = input("Digite a raça: ").strip()
        raca = next((nome for nome in racas_validas if nome.lower() == raca_digitada.lower()), None)

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
    print("\n===== GASTOS DE CRIAÇÃO =====")

    try:
        alimentacao = float(input("Custo total de alimentação (R$): "))
        vacinas = float(input("Custo com vacinas obrigatórias (R$): "))
        medicamentos = float(input("Custo com medicamentos opcionais (R$): "))
        frete = float(input("Custo com frete (R$): "))
        mao_de_obra = float(input("Custo com mão de obra (R$): "))
        documentacao = float(input("Custos com documentação e taxas (R$): "))
    except:
        print("Digite apenas números válidos para os gastos.")
        return [0, 0, 0, 0, 0, 0]

    return [alimentacao, vacinas, medicamentos, frete, mao_de_obra, documentacao]

def menu_venda(lote, lista_gastos, usuario_id):
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
    rendimento_medio = (lote["rendimento_min"] + lote["rendimento_max"]) / 2
    peso_carcaca = calcular_peso_carcaca(peso_venda, rendimento_medio * 100)
    arrobas_totais = calcular_arrobas(peso_carcaca) * lote["quantidade"]

    receita_bruta = calcular_receita_bruta(arrobas_totais, preco_arroba)
    total_impostos = calcular_total_impostos(receita_bruta, tipo_produtor, aliquota_icms)
    receita_liquida = calcular_receita_liquida(receita_bruta, total_impostos)
    gastos_totais = calcular_total_gastos(lista_gastos)
    custo_total = calcular_custo_total(lote["custo_compra_total"], lista_gastos)
    lucro_liquido = calcular_lucro_liquido(receita_liquida, custo_total)
    lucro_por_cabeca = calcular_lucro_por_cabeca(lucro_liquido, lote["quantidade"])
    ponto_equilibrio = calcular_ponto_equilibrio(custo_total, arrobas_totais)

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
        # resultados financeiros
        "receita_bruta":      receita_bruta,
        "total_impostos":     total_impostos,
        "receita_liquida":    receita_liquida,
        "gastos_totais":      gastos_totais,
        "custo_total":        custo_total,
        "lucro_liquido":      lucro_liquido,
        "lucro_por_cabeca":   lucro_por_cabeca,
        "ponto_equilibrio":   ponto_equilibrio,
    }

    exibir_resumo_lote(resultados)
    exibir_resultado_financeiro(resultados)
    exibir_alerta_lucro(resultados["lucro_liquido"], resultados["ponto_equilibrio"])
    salvar_resultado(resultados, usuario_id)

def menu_historico(usuario_id):
    historico = banco.buscar_historico(usuario_id)
    if not historico:
        print("Nenhum lote registrado ainda.")
        return
    print("\n===== HISTÓRICO DE LOTES =====")
    for raca, categoria, quantidade, lucro_liquido, data in historico:
        print(f"{data} — {quantidade}x {raca} ({categoria}) — Lucro líquido: R$ {lucro_liquido:.2f}")


if __name__ == "__main__":
    iniciar_sistema()
