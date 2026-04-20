import joblib
import pandas as pd
from loguru import logger

class RiskPredictor:
    """Interface para inferência com o modelo treinado."""
    
    def __init__(self, model_path: str = "models/trained/model.joblib"):
        try:
            self.model = joblib.load(model_path)
            logger.info(f"Modelo carregado de {model_path}")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
            raise

    def predict(self, input_data: pd.DataFrame) -> pd.Series:
        """Realiza a predição para novos dados."""
        return self.model.predict(input_data)

    def predict_proba(self, input_data: pd.DataFrame) -> pd.DataFrame:
        """Retorna as probabilidades de cada classe."""
        return self.model.predict_proba(input_data)
