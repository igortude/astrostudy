import pandas as pd
import numpy as np
from loguru import logger

class FeatureEngineer:
    """
    Transforma dados brutos em inteligência física para predição de risco.
    
    Como Cientistas de Dados Sêniores, não apenas 'limpamos' dados; nós criamos 
    novas representações que capturam a realidade física do problema.
    """
    
    @staticmethod
    def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
        """
        Executa o pipeline completo de Feature Engineering.
        """
        logger.info(f"Iniciando Feature Engineering em {len(df)} registros.")
        df_feat = df.copy()
        
        # Constante para evitar log(0)
        eps = 1e-10
        
        # 1. TRATAMENTO DE DIÂMETRO (Média Geométrica + Log)
        # INTUIÇÃO: A média geométrica é preferível para grandezas que variam 
        # exponencialmente (como o volume de objetos celestes).
        df_feat['diameter_km'] = np.sqrt(
            df_feat['diameter_min_km'] * df_feat['diameter_max_km']
        )
        df_feat['log_diameter'] = np.log10(df_feat['diameter_km'] + eps)
        
        # 2. VELOCIDADE (Log Transform)
        # INTUIÇÃO: A velocidade relativa varia muito. O log normaliza a 
        # distribuição e destaca ordens de magnitude.
        df_feat['log_velocity'] = np.log10(df_feat['velocity_km_s'] + eps)
        
        # 3. DISTÂNCIA (Log Transform)
        # INTUIÇÃO: Miss Distance está na casa dos milhões. O log coloca essa 
        # distância em uma escala comparável ao diâmetro e velocidade.
        df_feat['log_miss_distance'] = np.log10(df_feat['miss_distance_km'] + eps)
        
        # 4. ASTRORISK SCORE (Aproximação de Energia Cinética)
        # FÓRMULA: 3*log(d) + 2*log(v) - log(dist)
        # INTUIÇÃO FÍSICA: 
        # - E_cinetica ∝ massa * v²
        # - massa ∝ volume ∝ d³
        # - risco ∝ E_cinetica / distância (proximidade potencializa o dano)
        # Aplicando log: log(d³ * v² / dist) = 3log(d) + 2log(v) - log(dist)
        df_feat['astrorisk_score'] = (
            3 * df_feat['log_diameter'] + 
            2 * df_feat['log_velocity'] - 
            df_feat['log_miss_distance']
        )
        
        # 5. INCERTEZA (Uncertainty Ratio)
        # INTUIÇÃO: O quão incerta é a medição da NASA. Diâmetros muito 
        # incertos podem mascarar riscos maiores do que o reportado.
        df_feat['uncertainty_ratio'] = (
            (df_feat['diameter_max_km'] - df_feat['diameter_min_km']) / 
            (df_feat['diameter_min_km'] + eps)
        )
        
        # 6. FEATURES ADICIONAIS (Identidade)
        # Identificador composto para garantir que cada passagem do mesmo asteroide 
        # seja tratada como um evento orbital distinto.
        df_feat['event_id'] = df_feat['id'].astype(str) + "_" + df_feat['date'].astype(str)
        
        logger.success("Pipeline de Feature Engineering concluído com sucesso.")
        return df_feat
