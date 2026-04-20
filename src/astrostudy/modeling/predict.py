import joblib
import pandas as pd
import numpy as np
from loguru import logger
from pathlib import Path
from typing import Union, Dict, Any

from astrostudy.features.engineer import FeatureEngineer

class RiskPredictor:
    """
    Interface de alto nível para inferência de risco de asteroides.
    
    Esta classe encapsula o carregamento do modelo, o processamento de features
    e a lógica de predição, garantindo consistência entre treino e produção.
    
    NOTA: As probabilidades extremas (perto de 0 ou 1) observadas podem ser 
    resultado do tamanho reduzido do dataset atual ou da separação linear clara 
    das features e devem ser interpretadas com cautela em produção.
    """
    
    def __init__(self, model_path: str = "models/trained/optimized_baseline.joblib"):
        self.model_path = Path(model_path)
        self.required_inputs = [
            'diameter_min_km', 
            'diameter_max_km', 
            'velocity_km_s', 
            'miss_distance_km'
        ]
        self.features = [
            'log_diameter', 
            'log_velocity', 
            'log_miss_distance', 
            'astrorisk_score', 
            'uncertainty_ratio'
        ]
        self._load_model()

    def _load_model(self):
        """Carrega o modelo salvo usando joblib."""
        try:
            if not self.model_path.exists():
                raise FileNotFoundError(f"Modelo não encontrado em: {self.model_path}")
            
            self.model = joblib.load(self.model_path)
            logger.success(f"Modelo de risco carregado: {self.model_path}")
        except Exception as e:
            logger.error(f"Falha crítica ao carregar o modelo: {str(e)}")
            raise

    def _validate_input(self, data: Dict):
        """Valida se os campos obrigatórios estão presentes e são válidos."""
        missing = [field for field in self.required_inputs if field not in data]
        if missing:
            logger.error(f"Dados incompletos. Faltam os campos: {missing}")
            raise ValueError(f"Campos obrigatórios ausentes: {missing}")
        
        # Verificação simples de tipos/valores
        for field in self.required_inputs:
            try:
                val = float(data[field])
                if val < 0:
                    raise ValueError(f"O campo {field} não pode ser negativo.")
            except (ValueError, TypeError):
                raise ValueError(f"O campo {field} deve ser um número válido.")

    def _categorize_risk(self, probability: float) -> str:
        """
        Transforma a probabilidade contínua em categorias de risco de negócio.
        """
        if probability < 0.15:
            return "Low Risk"
        elif probability < 0.60:
            return "Moderate Risk"
        else:
            return "High Risk"

    def _preprocess(self, data: Union[Dict, pd.DataFrame]) -> pd.DataFrame:
        """
        Transforma dados de entrada no formato esperado pelo modelo com validação.
        """
        if isinstance(data, dict):
            self._validate_input(data)
            df = pd.DataFrame([data])
        else:
            for _, row in data.iterrows():
                self._validate_input(row.to_dict())
            df = data.copy()

        # Aplicar Feature Engineering
        df_featured = FeatureEngineer.engineer_features(df)
        return df_featured[self.features]

    def predict(self, data: Union[Dict, pd.DataFrame]) -> Dict[str, Any]:
        """
        Realiza a predição completa com categorização de risco e logs detalhados.
        """
        try:
            # 1. Preprocessamento
            X = self._preprocess(data)
            
            # 2. Inferência
            probabilities = self.model.predict_proba(X)[:, 1]
            predictions = self.model.predict(X)
            
            # 3. Formatação do Resultado
            if len(X) == 1:
                prob = float(probabilities[0])
                pred = int(predictions[0])
                risk_level = self._categorize_risk(prob)
                
                # Recuperar features geradas
                # Usamos .iloc[0] para pegar o primeiro (e único) registro
                features_dict = X.iloc[0].to_dict()
                
                result = {
                    "probability": prob,
                    "prediction": pred,
                    "risk_level": risk_level,
                    "is_hazardous": bool(pred),
                    "features": features_dict
                }
                
                logger.info(f"Inferência: Prob={prob:.4f} | Nível={risk_level} | Hazardous={pred}")
                return result
            
            # Múltiplos registros
            results = []
            for i, (p, pred) in enumerate(zip(probabilities, predictions)):
                results.append({
                    "probability": float(p),
                    "risk_level": self._categorize_risk(float(p)),
                    "is_hazardous": bool(pred),
                    "features": X.iloc[i].to_dict()
                })
            return {"results": results}

        except Exception as e:
            logger.error(f"Erro durante a inferência: {str(e)}")
            raise

def predict_asteroid_risk(data: Dict) -> Dict:
    """
    Função utilitária profissional para integração.
    """
    predictor = RiskPredictor()
    return predictor.predict(data)
