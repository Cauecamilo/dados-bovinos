import sqlite3
import matplotlib.pyplot as plt
import numpy as np


def gerar_grafico_lucro_equilibrio(usuario_id):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    # Busca o Ponto de Equilíbrio e o Preço de Venda por arroba de cada lote
    cursor.execute(
        """
        SELECT id, raca, ponto_equilibrio, preco_arroba
        FROM resultados_lote
        WHERE usuario_id = ?
        ORDER BY id ASC
    """,
        (usuario_id,),
    )

    dados = cursor.fetchall()
    conexao.close()

    if not dados:
        print("Nenhum lote encontrado para gerar o gráfico.")
        return False

    # Estruturação dos dados
    rotulos_lotes = [
        f"Lote {i}\n({item[1]})" for i, item in enumerate(dados, start=1)
    ]
    pontos_equilibrio = [item[2] for item in dados]
    precos_venda = [item[3] for item in dados]

    # Definição das posições e largura das barras
    x = np.arange(len(rotulos_lotes))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))

    # Desenho das barras 
    barras_pe = ax.bar(
        x - largura / 2,
        pontos_equilibrio,
        largura,
        label="Ponto de Equilíbrio (Custo R$/@)",
        color="#d9534f",  # Vermelho
    )
    barras_pv = ax.bar(
        x + largura / 2,
        precos_venda,
        largura,
        label="Preço de Venda Obtido (R$/@)",
        color="#5cb85c",  # Verde
    )

    # Títulos e formatação dos eixos
    ax.set_ylabel("Valor por Arroba (R$/@)", fontsize=11, fontweight="bold")
    ax.set_xlabel(
        "Lotes Cadastrados", fontsize=11, fontweight="bold", labelpad=10
    )
    ax.set_title(
        "Comparativo de Eficiência: Ponto de Equilíbrio vs. Preço de Venda",
        fontsize=13,
        fontweight="bold",
        pad=15,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(rotulos_lotes)
    ax.legend(loc="upper left")
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    # Função para escrever os valores em R$ no topo de cada barra
    def adicionar_rotulos(barras, cor):
        for barra in barras:
            altura = barra.get_height()
            texto = f"R$ {altura:.2f}".replace(".", ",")
            ax.annotate(
                texto,
                xy=(barra.get_x() + barra.get_width() / 2, altura),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=9,
                fontweight="bold",
                color=cor,
            )

    adicionar_rotulos(barras_pe, "#a94442")
    adicionar_rotulos(barras_pv, "#3c763d")

    plt.tight_layout()
    plt.show()