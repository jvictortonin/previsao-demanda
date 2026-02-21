import pandas as pd
import numpy as np

np.random.seed(42)

# =============================
# PARÂMETROS
# =============================
datas = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")

clientes = [
    "Construtora Alfa",
    "Esquadrias Brasil",
    "SolarTech",
    "Metalúrgica Omega",
    "Vidraçaria União"
]

produtos = [
    "Perfil U",
    "Perfil I",
    "Perfil Tubular",
    "Cantoneira",
    "Barra Chata",
    "Trilho"
]

# demanda base por produto
base_produto = {
    "Perfil U": 1200,
    "Perfil I": 900,
    "Perfil Tubular": 750,
    "Cantoneira": 600,
    "Barra Chata": 500,
    "Trilho": 650
}

dados = []

for data in datas:
    mes = data.month

    # fator sazonal (ex: construção civil cresce no meio do ano)
    fator_sazonal = 1.2 if mes in [5,6,7,8,9] else 0.9

    for cliente in clientes:
        for produto in produtos:

            tendencia = 1 + (data.year - 2024) * 0.05

            ruido = np.random.normal(1, 0.15)

            quantidade = (
                base_produto[produto]
                * fator_sazonal
                * tendencia
                * ruido
            )

            quantidade = max(0, round(quantidade, 0))

            dados.append([
                data,
                cliente,
                produto,
                quantidade
            ])

df = pd.DataFrame(dados, columns=[
    "Data", "Cliente", "Produto", "Quantidade (kg)"
])

df.to_excel("historico_demanda_24_meses.xlsx", index=False)

print("Dataset gerado com sucesso!")
