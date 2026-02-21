import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def carregar_e_processar_dados(arquivo):
    df = pd.read_excel(arquivo)
    df['Data'] = pd.to_datetime(df['Data'])
    
    # Agregar por Mês e Produto
    df['Mes_Ano'] = df['Data'].dt.to_period('M')
    df_agrupado = df.groupby(['Mes_Ano', 'Produto'])['Quantidade (kg)'].sum().reset_index()
    
    # Converter Mes_Ano de volta para timestamp para extrair features
    df_agrupado['Data_Ref'] = df_agrupado['Mes_Ano'].dt.to_timestamp()
    
    # Criar features temporais
    df_agrupado['Mes'] = df_agrupado['Data_Ref'].dt.month
    df_agrupado['Ano'] = df_agrupado['Data_Ref'].dt.year
    df_agrupado['Timestamp_Ord'] = df_agrupado['Data_Ref'].map(pd.Timestamp.toordinal)
    
    return df_agrupado

def treinar_e_prever(df):
    produtos = df['Produto'].unique()
    resultados = []
    
    # Identificar os últimos 3 meses do dataset para teste
    meses_unicos = df['Mes_Ano'].unique()
    meses_teste = meses_unicos[-3:]
    
    print(f"Período de Teste (Validação): {meses_teste}")
    
    for produto in produtos:
        df_prod = df[df['Produto'] == produto].copy()
        
        # Separar Treino e Teste
        mask_teste = df_prod['Mes_Ano'].isin(meses_teste)
        df_treino = df_prod[~mask_teste]
        df_teste = df_prod[mask_teste]
        
        if df_teste.empty:
            print(f"Aviso: Sem dados de teste para o produto {produto}")
            continue
            
        # Features para o modelo
        features = ['Mes', 'Ano', 'Timestamp_Ord']
        target = 'Quantidade (kg)'
        
        X_train = df_treino[features]
        y_train = df_treino[target]
        X_test = df_teste[features]
        y_test_real = df_teste[target]
        
        # Modelo Random Forest
        modelo = RandomForestRegressor(n_estimators=100, random_state=42)
        modelo.fit(X_train, y_train)
        
        # Previsão
        previsoes = modelo.predict(X_test)
        
        # Organizar resultados
        for data_ref, real, pred in zip(df_teste['Data_Ref'], y_test_real, previsoes):
            resultados.append({
                'Produto': produto,
                'Data': data_ref.strftime('%Y-%m'),
                'Real': real,
                'Previsto': round(pred, 2),
                'Erro Absoluto': round(abs(real - pred), 2),
                'Erro (%)': round(abs(real - pred) / real * 100, 2) if real != 0 else 0
            })

    return pd.DataFrame(resultados)

if __name__ == "__main__":
    arquivo_entrada = "historico_demanda_24_meses.xlsx"
    
    print("Carregando dados...")
    try:
        df = carregar_e_processar_dados(arquivo_entrada)
        
        print("Treinando modelos e gerando previsões...")
        df_resultados = treinar_e_prever(df)
        
        print("\n=== Resultados da Validação (Últimos 3 Meses) ===")
        print(df_resultados.to_string(index=False))
        
        # Calcular erro médio global
        mae_global = df_resultados['Erro Absoluto'].mean()
        mape_global = df_resultados['Erro (%)'].mean()
        
        print(f"\nErro Médio Absoluto (Global): {mae_global:.2f}")
        print(f"Erro Percentual Médio (Global): {mape_global:.2f}%")
        
        df_resultados.to_excel("validacao_previsao.xlsx", index=False)
        print("\nDetalhes salvos em 'validacao_previsao.xlsx'")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado. Gere o dataset primeiro.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
