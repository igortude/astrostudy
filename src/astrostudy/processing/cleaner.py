import pandas as pd
from loguru import logger
import json
from pathlib import Path

class DataCleaner:
    """
    Limpeza e normalização dos dados brutos coletados da NASA.
    Responsável por transformar JSONs aninhados em uma estrutura tabular limpa.
    """
    
    @staticmethod
    def load_and_flatten(raw_dir: str = "data/raw") -> pd.DataFrame:
        """
        Lê todos os arquivos JSON na pasta raw e extrai os asteroides.
        """
        raw_path = Path(raw_dir)
        all_asteroids = []
        
        json_files = list(raw_path.glob("*.json"))
        logger.info(f"Limpando {len(json_files)} arquivos da camada raw.")
        
        for file in json_files:
            with open(file, 'r', encoding='utf-8') as f:
                content = json.load(f)
                
                # Lembra que nosso DataSaver salva em {"data": {"date": "...", "asteroids": [...]}}
                date_str = content.get("data", {}).get("date")
                asteroids = content.get("data", {}).get("asteroids", [])
                
                for ast in asteroids:
                    # Extração segura dos campos aninhados
                    close_approach = ast.get("close_approach_data", [{}])[0]
                    
                    clean_obj = {
                        "id": ast.get("id"),
                        "name": ast.get("name"),
                        "date": date_str,
                        "is_hazardous": ast.get("is_potentially_hazardous_asteroid"),
                        "diameter_min_km": ast.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_min"),
                        "diameter_max_km": ast.get("estimated_diameter", {}).get("kilometers", {}).get("estimated_diameter_max"),
                        "velocity_km_s": float(close_approach.get("relative_velocity", {}).get("kilometers_per_second", 0)),
                        "miss_distance_km": float(close_approach.get("miss_distance", {}).get("kilometers", 0)),
                    }
                    all_asteroids.append(clean_obj)
        
        df = pd.DataFrame(all_asteroids)
        # Drop duplicatas se houver (mesmo asteroide na mesma data em arquivos diferentes)
        df = df.drop_duplicates(subset=['id', 'date'])
        
        logger.info(f"Limpeza concluída. {len(df)} registros tabulares gerados.")
        return df
