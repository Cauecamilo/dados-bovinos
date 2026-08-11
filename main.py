import banco
from calculos import *
from dados import *
from banco import *
from dotenv import load_dotenv
from google import genai


def iniciar_sistema():
    print("=" * 50)
    print("SISTEMA DE GESTÃO PECUÁRIA BOVINA".center(50))
    print("Controle completo do seu rebanho".center(50))
    print("=" * 50)
    usuario_id = fazer_login_ou_cadastro()
    opcao = ""

    while opcao != "3":
        opcao = menu_principal()

        if opcao == "1":
            sub_menu_lote(usuario_id)   
        elif opcao == "2":
            menu_historico(usuario_id)

        elif opcao == "3":
            print("Encerrando o sistema. Até logo!")

        else:
            print("Opção inválida. Digite 1, 2 ou 3.")


def fazer_login_ou_cadastro():
    while True:
        print("\n" + "=" * 50)
        print("ACESSO AO SISTEMA".center(50))
        print("=" * 50)
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
                print(f"Credenciais inválidas. Tentativas restantes: {3 - tentativas}")
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
    print("\n" + "=" * 50)
    print("MENU PRINCIPAL".center(50))
    print("=" * 50)
    print("1. Gerenciar Lote       → cadastrar e vender")
    print("2. Ver Histórico        → lotes anteriores")
    print("3. Sair")
    print("=" * 50)
    opcao = input("Escolha uma opção: ")
    return opcao

def sub_menu_lote(usuario_id):
    lote = None
    lista_gastos = []
    venda_realizada = False
    opcao = ""

    while opcao != "6":
        print("\n" + "=" * 50)
        print("GERENCIAMENTO DE LOTE".center(50))
        print("=" * 50)
        print("1. Cadastrar Lote       → registrar novo lote")
        print("2. Ver Estimativa       → projeção de resultado")
        print("3. Registrar Gastos     → custos de criação")
        print("4. Registrar Venda      → finalizar o lote")
        print("5. Análise da IA        → diagnóstico do resultado")
        print("6. Voltar")
        print("=" * 50)
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            lote = menu_lote()
            print("\n" + "=" * 50)
            print("✔ Lote cadastrado com sucesso!".center(50))
            print("=" * 50)
            print("→ Veja a estimativa (opção 2) ou")
            print("  registre os gastos (opção 3).")

        elif opcao == "2":
            if lote is None:
                print("Cadastre o lote primeiro (opção 1).")
            else:
                exibir_estimativa(lote)

        elif opcao == "3":
            if lote is None:
                print("Cadastre o lote primeiro (opção 1).")
            else:
                lista_gastos = menu_gastos()

        elif opcao == "4":
            if lote is None:
                print("Cadastre o lote primeiro (opção 1).")
            elif not lista_gastos:
                print("Registre os gastos primeiro (opção 3).")
            elif venda_realizada:
                print("Venda já registrada para este lote.")
            else:
                menu_venda(lote, lista_gastos, usuario_id)
                venda_realizada = True

        elif opcao == "5":
            if not venda_realizada:
                print("Registre a venda primeiro (opção 4).")
            else:
                meta = lote.get("peso_carcaca_estimado", None)
                if meta is None:
                    print("Estime o lote primeiro (opção 2) antes de analisar.")
                else:
                    resultado = analise_ia(lote["peso_carcaca_real"], lote["raca"], meta)
                    if resultado:
                        print("\n===== ANÁLISE DA IA =====")
                        print(resultado)
                        print("===========================")
                    else:
                        print("O peso de carcaça ficou dentro ou acima da meta. Nenhuma análise necessária.")

        elif opcao == "6":
            print("Voltando ao menu principal...")

        else:
            print("Opção inválida.")

def menu_lote():
    print("\n" + "=" * 50)
    print("CADASTRO DO LOTE".center(50))
    print("Informe os dados de compra do rebanho.".center(50))
    print("=" * 50)

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
    while quantidade <= 0 or quantidade > QUANTIDADE_MAXIMA:
        try:
            quantidade = int(input("Quantidade de animais: "))
            if quantidade <= 0 or quantidade > QUANTIDADE_MAXIMA:
                print(f"Digite um número entre 1 e {QUANTIDADE_MAXIMA}.")
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
    while dias < CICLO_MINIMO_DIAS or dias > CICLO_MAXIMO_DIAS:
        try:
            dias = int(input("Tempo estimado de criação (dias): "))
            if dias < CICLO_MINIMO_DIAS or dias > CICLO_MAXIMO_DIAS:
                print(f"Digite um valor entre {CICLO_MINIMO_DIAS} e {CICLO_MAXIMO_DIAS} dias.")
        except:
            print("Digite apenas números inteiros.")

    lote = cadastrar_lote(raca, categoria, quantidade, peso_compra, preco_compra)
    lote["dias_criacao"] = dias

    print("\n" + "=" * 50)
    print("RESUMO DO CADASTRO".center(50))
    print("=" * 50)
    print(f"  Raça:              {raca}")
    print(f"  Categoria:         {categoria}")
    print(f"  Quantidade:        {quantidade} animais")
    print(f"  Dias de criação:   {dias}")
    print(f"  Custo total:       R$ {quantidade * preco_compra:.2f}")
    print("=" * 50)
    return lote

def menu_gastos():
    print("\n" + "=" * 50)
    print("GASTOS DE CRIAÇÃO".center(50))
    print("Digite 0 caso não tenha tido esse gasto.".center(50))
    print("=" * 50)

    alimentacao  = pedir_valor("Custo total de alimentação (R$): ")
    vacinas      = pedir_valor("Custo com vacinas obrigatórias (R$): ")
    medicamentos = pedir_valor("Custo com medicamentos opcionais (R$): ")
    frete        = pedir_valor("Custo com frete (R$): ")
    mao_de_obra  = pedir_valor("Custo com mão de obra (R$): ")
    documentacao = pedir_valor("Custos com documentação e taxas (R$): ")

    total = sum([alimentacao, vacinas, medicamentos, frete, mao_de_obra, documentacao])
    print("\n" + "=" * 50)
    print(f"Total de gastos: R$ {total:.2f}".center(50))
    print("=" * 50)
    return [alimentacao, vacinas, medicamentos, frete, mao_de_obra, documentacao]

def menu_venda(lote, lista_gastos, usuario_id):
    print("\n" + "=" * 50)
    print("REGISTRO DE VENDA".center(50))
    print("Informe os dados reais da venda.".center(50))
    print("=" * 50)

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
        print("\nTipo de produtor:")
        print("  PF → Pessoa Física")
        print("  PJ → Pessoa Jurídica")
        print("  SE → Segurado Especial")
        tipo_produtor = input("Digite PF, PJ ou SE: ").upper()
        tipo_produtor = input("Tipo de produtor (PF/PJ/SE): ").upper()
        if tipo_produtor not in opcoes_validas:
            print("Opção inválida.")

    opcoes_estado = ["SIM", "NAO"]
    mesmo_estado = ""

    while mesmo_estado not in opcoes_estado:
        mesmo_estado = input("A venda é para dentro do mesmo estado? (SIM/NAO): ").upper()
        if mesmo_estado not in opcoes_estado:
            print("Digite SIM ou NAO.")

    if mesmo_estado == "NAO":
        aliquota_icms = ICMS_INTERESTADUAL
    else:
        aliquota_icms = 0

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

    lote["peso_carcaca_real"] = peso_carcaca
    exibir_resumo_lote(resultados)
    exibir_resultado_financeiro(resultados)
    exibir_alerta_lucro(resultados["lucro_liquido"], resultados["ponto_equilibrio"])
    salvar_resultado(resultados, usuario_id)

def analise_ia(peso_carcaca, raca_boi, meta_peso_carcaca):
    if peso_carcaca < meta_peso_carcaca:
        diferenca_meta = meta_peso_carcaca - peso_carcaca

        prompt = f"""
            Você é um zootecnista sênior e consultor em manejo de bovinocultura de corte.

            DADOS PARA ANÁLISE:
            - Raça do gado: {raca_boi}
            - Peso de carcaça obtido: {peso_carcaca:.2f} kg
            - Peso de carcaça esperado (Meta): {meta_peso_carcaca:.2f} kg
            - Déficit de peso: {diferenca_meta:.2f} kg

            TAREFA:
            1. CLASSIFICAÇÃO DE GRAVIDADE: Classifique a perda de {diferenca_meta:.2f} kg (Leve, Moderada ou Crítica).
            2. ANÁLISE DE RAÇA: Avalie o desempenho para a raça {raca_boi}.
            3. CAUSAS PROVÁVEIS: Liste exatamente 3 causas prováveis.
            4. PLANO DE AÇÃO: Recomende 2 ações imediatas para a raça {raca_boi}.

            Responda de forma técnica, direta e em tópicos.
            """
        try:
            client = genai.Client()
            resposta = client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return resposta.text
        except Exception as e:
            return f"Erro na API do Gemini: {e}"

    return None

def menu_historico(usuario_id):
    historico = banco.buscar_historico(usuario_id)
    if not historico:
        print("Nenhum lote registrado ainda.")
        return
    print("\n===== HISTÓRICO DE LOTES =====")
    for raca, categoria, quantidade, lucro_liquido, data in historico:
        print(f"{data} — {quantidade}x {raca} ({categoria}) — Lucro líquido: R$ {lucro_liquido:.2f}")


if __name__ == "__main__":
    load_dotenv()
    iniciar_sistema()
