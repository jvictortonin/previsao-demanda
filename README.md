# 📊 Previsão de Demanda

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Random%20Forest-orange?logo=scikitlearn&logoColor=white)

Sistema de **previsão de demanda** de produtos utilizando **Random Forest Regressor** (scikit-learn). Ideal para distribuidoras e indústrias que desejam antecipar a demanda com base em dados históricos de vendas.

## ✨ Funcionalidades

- **Geração de dados sintéticos** — cria um dataset realista de 24 meses com sazonalidade e tendência
- **Previsão com Machine Learning** — modelo Random Forest treinado com features temporais
- **Validação automática** — compara previsões com dados reais dos últimos 3 meses
- **Métricas de erro** — calcula MAE e MAPE por produto e global
- **Exportação** — resultados salvos em Excel (`.xlsx`)

## 📁 Estrutura do Projeto

```
previsao-demanda/
├── gera_dataset.py          # Geração do dataset sintético (24 meses)
├── previsao_demanda.py      # Modelo de previsão e validação
├── requirements.txt         # Dependências do projeto
├── LICENSE                  # Licença MIT
└── README.md                # Documentação
```

## 🔧 Pré-requisitos

- **Python 3.8** ou superior
- **pip** (gerenciador de pacotes)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/<SEU_USUARIO>/previsao-demanda.git
cd previsao-demanda
```

2. (Opcional) Crie um ambiente virtual:
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📖 Como Usar

### Passo 1 — Gerar o Dataset

Gera um arquivo Excel com 24 meses de dados históricos de demanda:

```bash
python gera_dataset.py
```

Saída: `historico_demanda_24_meses.xlsx`

### Passo 2 — Executar a Previsão

Treina o modelo e valida as previsões contra os últimos 3 meses:

```bash
python previsao_demanda.py
```

Saída: `validacao_previsao.xlsx`

### Exemplo de Saída

```
Carregando dados...
Treinando modelos e gerando previsões...

=== Resultados da Validação (Últimos 3 Meses) ===
  Produto       Data      Real   Previsto  Erro Absoluto  Erro (%)
 Perfil U    2025-10  27540.00   28102.35         562.35      2.04
 Perfil I    2025-10  21330.00   20987.12         342.88      1.61
     ...        ...       ...        ...           ...       ...

Erro Médio Absoluto (Global): 487.23
Erro Percentual Médio (Global): 2.85%
```

## 🧠 Como Funciona

1. **Geração de dados** (`gera_dataset.py`): cria vendas diárias para 5 clientes e 6 produtos com sazonalidade (meses 5–9 mais fortes) e tendência de crescimento de 5% ao ano.

2. **Previsão** (`previsao_demanda.py`):
   - Agrega dados por mês e produto
   - Cria features temporais (mês, ano, ordinal)
   - Treina um **Random Forest** (100 árvores) por produto
   - Valida previsões nos últimos 3 meses do histórico
   - Calcula erro absoluto e percentual

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| **pandas** | Manipulação de dados |
| **numpy** | Geração de dados sintéticos |
| **scikit-learn** | Modelo Random Forest |
| **openpyxl** | Leitura/escrita de Excel |

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
