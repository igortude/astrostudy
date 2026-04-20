import json
import pandas as pd
from pathlib import Path
from loguru import logger

def deep_investigation(data_dir: str = "data/raw"):
    raw_path = Path(data_dir)
    json_files = list(raw_path.glob("*.json"))
    
    all_asteroids_flat = []
    
    # Vamos analisar a estrutura de 'close_approach_data' e duplicidade de IDs
    asteroid_id_counts = {}
    approach_list_lengths = []
    
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            asteroids = content.get("data", {}).get("asteroids", [])
            
            for ast in asteroids:
                ast_id = ast.get("id")
                asteroid_id_counts[ast_id] = asteroid_id_counts.get(ast_id, 0) + 1
                
                approaches = ast.get("close_approach_data", [])
                approach_list_lengths.append(len(approaches))
                
                # Vamos registrar o conteúdo da primeira aproximação para ver a data
                if approaches:
                    all_asteroids_flat.append({
                        "id": ast_id,
                        "file_date": content.get("data", {}).get("date"),
                        "approach_date": approaches[0].get("close_approach_date"),
                        "approach_count": len(approaches)
                    })

    df_investigation = pd.DataFrame(all_asteroids_flat)
    
    print("\n--- 🔍 INVESTIGAÇÃO DE PROFUNDIDADE ---")
    
    # 1. Análise de Close Approach Data
    max_len = max(approach_list_lengths) if approach_list_lengths else 0
    avg_len = sum(approach_list_lengths)/len(approach_list_lengths) if approach_list_lengths else 0
    print(f"\n1. Close Approach Data:")
    print(f"   - Tamanho máximo da lista: {max_len}")
    print(f"   - Tamanho médio da lista: {avg_len:.2f}")
    
    # 2. Asteroides Repetidos (Duplicidade)
    duplicates = {k: v for k, v in asteroid_id_counts.items() if v > 1}
    print(f"\n2. Asteroides Repetidos:")
    print(f"   - Total de IDs únicos: {len(asteroid_id_counts)}")
    print(f"   - Total de IDs repetidos entre arquivos: {len(duplicates)}")
    if duplicates:
        print(f"   - Exemplos de IDs repetidos: {list(duplicates.keys())[:5]}")

    # 3. Verificação de Datas
    # Queremos saber se a data do arquivo (coleta) coincide com a data da aproximação
    mismatches = df_investigation[df_investigation['file_date'] != df_investigation['approach_date']]
    print(f"\n3. Consistência de Datas:")
    print(f"   - Registros onde Data do Arquivo != Data de Aproximação: {len(mismatches)}")
    if not mismatches.empty:
        print("   - Exemplo de mismatch:")
        print(mismatches.head(3))

if __name__ == "__main__":
    deep_investigation()
