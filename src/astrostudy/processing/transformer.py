import pandas as pd
from loguru import logger
from sklearn.preprocessing import StandardScaler

class DataTransformer:
    """Transformação e normalização de dados."""
    
    def __init__(self):
        self.scaler = StandardScaler()
    
    def apply_scaling(self, df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        """Aplica normalização Standard às colunas selecionadas."""
        logger.info(f"Aplicando scaling nas colunas: {columns}")
        df_scaled = df.copy()
        df_scaled[columns] = self.scaler.fit_transform(df[columns])
        return df_scaled
