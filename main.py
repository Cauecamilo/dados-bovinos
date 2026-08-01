
from calculos import *
from dados import *
from banco import *

def menu_principal():
    pass

def menu_lote():
    pass

def menu_gastos():
    pass

def menu_venda():
    pass

def menu_historico():
    pass

def iniciar_sistema():
    pass

iniciar_sistema()

def arrumar_entrada(entrada):
    return entrada.strip().replace("." , "").replace(',', '.')

def receber_calculos_peso_carcaca():
    print("=== ENTRADA DE DADOS DO ANIMAL ===")
    
    peso_vivo = float(arrumar_entrada(input("Digite o peso vivo do animal (kg): ")))

    while peso_vivo <= 0:
        print("ERRO: Digite o valor do peso maior que zero!")
        peso_vivo = float(arrumar_entrada(input("Digite um peso válido para o animal (kg): ")))

    rendimento_percentual = float(arrumar_entrada(input("Digite o rendimento percentual (%): ")))
    
    while rendimento_percentual <= 0 or rendimento_percentual > 100:
        print("ERRO: Digite um valor maior que zero e igual ou menor que cem!")
        rendimento_percentual = float(arrumar_entrada(input("Digite um valor válido para o rendimento percentual: ")))
    
    horas_viagem = int(arrumar_entrada(input("Digite a quantidade apenas de horas que levou o transporte: ")))
    
    while horas_viagem <= 0:
        print("ERRO: Digite a quantidade de horas maior que zero!")
        horas_viagem = int(arrumar_entrada(input("Digite a quantidade válida apenas de horas que levou o transporte: ")))
    
    minutos_viagem = int(arrumar_entrada(input("Digite a quantidade apenas de minutos do transporte (0 a 59):")))
    
    while minutos_viagem > 59 or minutos_viagem < 0:
        print("ERRO: Digite a quantidade de minutos maior que zero e menor ou igual a cinquenta e nove!")
        minutos_viagem = int(arrumar_entrada(input("Digite a quantidade válida apenas de minutos do transporte")))
    
    horas_totais = horas_viagem + (minutos_viagem / 60)
    
    peso_inicial = float(arrumar_entrada(input("Digite o valor do peso inicial do animal: ")))
    
    while peso_inicial <= 0:
        print("ERRO: Digite o valor do peso inicial maior que zero!")
        peso_inicial = float(arrumar_entrada(input("Digite um valor válido para peso inicial: ")))
    
    gmd = float(arrumar_entrada(input("Digite o valor de ganho médio diário (gmd) do animal: ")))
    
    while gmd <= 0:
        print("ERRO: Digite um valor de ganho médio diário (gmd) maior que zero!")
        gmd = float(arrumar_entrada(input("Digite o valor válido de ganho médio diário (gmd) do animal: ")))
        
    dias = int(arrumar_entrada(input("Digite a quantidade de dias que o animal passou confinado: ")))
    
    while dias <= 0:
        print("ERRO: Digite a quantidade de dias maior que zero!")
        dias = int(arrumar_entrada(input("Digite a quantidade válida de dias que o animal passou confinado: ")))
    
    peso_carcaca = calcular_peso_carcaca(peso_vivo, rendimento_percentual)
    arrobas = calcular_arrobas(peso_carcaca)
    perda_transporte = calcular_perda_transporte(peso_vivo, horas_totais)
    peso_final = estimar_peso_final(peso_inicial, gmd, dias) 