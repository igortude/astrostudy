import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from loguru import logger

# Configurações de Estilo para Visualização
# POR QUE: Visualização clara é essencial para identificar padrões e outliers.
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

def load_raw_data(data_dir: str = "data/raw") -> pd.DataFrame:
    """
    Carrega múltiplos arquivos JSON da pasta raw e os consolida em um DataFrame único.
    
    ESTRATÉGIA: Como os dados são aninhados, precisamos 'achatar' (flatten) a estrutura
    para extrair o que realmente importa para a análise.
    """
    raw_path = Path(data_dir)
    all_asteroids = []
    
    json_files = list(raw_path.glob("*.json"))
    logger.info(f"Encontrados {len(json_files)} arquivos para análise.")
    
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
            # Recupera os dados de auditoria que adicionamos na ingestão
            collection_date = content.get("metadata", {}).get("date", "Unknown")
            
            # Extrai a lista de asteroides do dia
            asteroids = content.get("data", {}).get("asteroids", [])
            
            for ast in asteroids:
                # Extraindo apenas campos relevantes para a EDA
                # POR QUE: O JSON original tem muita informação de links e metadados da NASA
                # que não servem para modelagem estatística.
                
                # Close Approach Data é uma lista, pegamos a primeira entrada (a mais relevante)
                close_approach = ast.get("close_approach_data", [{}])[0]
                
                asteroid_data = {
                    "id": ast.get("id"),
                    "name": ast.get("name"),
                    "date": content.get("data", {}).get("date"),
                    "absolute_magnitude": ast.get("absolute_magnitude_h"),
                    "is_hazardous": ast.get("is_potentially_hazardous_asteroid"),
                    "diameter_min_km": ast.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min"),
                    "diameter_max_km": ast.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max"),
                    "velocity_km_s": float(close_approach.get("relative_velocity", {}).get("kilometers_per_second", 0)),
                    "miss_distance_km": float(close_approach.get("miss_distance", {}).get("kilometers", 0)),
                    "is_sentry": ast.get("is_sentry_object")
                }
                all_asteroids.append(asteroid_data)
                
    return pd.DataFrame(all_asteroids)

def perform_eda(df: pd.DataFrame):
    """
    Executa a análise exploratória e gera insights sobre a qualidade e distribuição dos dados.
    """
    print("\n--- 1. VISÃO GERAL DOS DADOS ---")
    print(f"Total de registros coletados: {len(df)}")
    print(f"Número de colunas: {len(df.columns)}")
    print("\nPrimeras 5 linhas:")
    print(df.head())
    
    print("\n--- 2. ANÁLISE DE QUALIDADE (VALORES NULOS) ---")
    # POR QUE: Nulos podem quebrar modelos de ML. Precisamos saber se a API falhou em algum campo.
    null_counts = df.isnull().sum()
    print(null_counts[null_counts > 0] if null_counts.any() else "Nenhum valor nulo encontrado.")

    print("\n--- 3. ESTATÍSTICA DESCRITIVA ---")
    # POR QUE: Entender a escala (média, desvio padrão) ajuda a identificar outliers e 
    # decidir sobre normalização futura.
    print(df.describe())

    print("\n--- 4. ALVO (TARGET): OBJETOS PERIGOSOS ---")
    # POR QUE: O desbalanceamento de classes é um desafio comum em detecção de risco.
    hazardous_counts = df['is_hazardous'].value_counts()
    hazardous_pct = df['is_hazardous'].value_counts(normalize=True) * 100
    print(f"Potencialmente Perigosos:\n{hazardous_counts}")
    print(f"Proporção: {hazardous_pct[True]:.2f}% de objetos são perigosos.")

    # --- VISUALIZAÇÕES ---
    
    # Gráfico 1: Quantidade por Dia
    plt.figure(figsize=(10, 5))
    df.groupby('date').size().plot(kind='bar', color='skyblue')
    plt.title("Quantidade de Asteroides Coletados por Dia")
    plt.ylabel("Contagem")
    plt.xticks(rotation=45)
    plt.savefig("models/reports/asteroids_by_day.png")
    
    # Gráfico 2: Distribuição de Diâmetro vs Velocidade (Colorido por Risco)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="diameter_max_km", y="velocity_km_s", hue="is_hazardous", style="is_hazardous")
    plt.title("Relação Diâmetro vs Velocidade (Colorido por Risco)")
    plt.savefig("models/reports/diameter_vs_velocity.png")

    # Gráfico 3: Distribuição da Distância de Aproximação
    plt.figure(figsize=(10, 5))
    sns.histplot(df['miss_distance_km'], kde=True, color='orange')
    plt.title("Distribuição da Distância de Aproximação (Miss Distance)")
    plt.savefig("models/reports/miss_distance_dist.png")

    print("\n--- 5. OBSERVAÇÕES PARA O CIENTISTA DE DADOS ---")
    print("1. [OUTLIERS]: Verifique se as velocidades extremas são erros de sensor ou casos raros.")
    print("2. [DESBALANCEAMENTO]: A classe 'hazardous' é minoritária. Pode ser necessário SMOTE ou ajuste de pesos.")
    print("3. [COLINEARIDADE]: diameter_min e diameter_max são quase idênticos (correlação ~1). Use apenas um ou a média.")
    print("4. [ESCALA]: Miss distance está em milhões de km, enquanto diâmetro está em frações. Normalização será OBRIGATÓRIA.")

if __name__ == "__main__":
    # Garante que a pasta de reports existe para salvar os gráficos
    Path("models/reports").mkdir(parents=True, exist_ok=True)
    
    df_asteroids = load_raw_data()
    if not df_asteroids.empty:
        perform_eda(df_asteroids)
    else:
        print("Nenhum dado encontrado em data/raw/ para análise.")
