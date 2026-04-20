import sys
from pathlib import Path

# Adicionar o diretório src ao path para permitir imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from astrostudy.modeling.predict import RiskPredictor, predict_asteroid_risk
from loguru import logger

def test_inference():
    logger.info("🚀 Iniciando Testes de Inferência Profissionais")
    
    # 1. Dados de um asteroide aparentemente seguro (pequeno e longe)
    safe_asteroid = {
        "id": "12345",
        "name": "Safe Rock",
        "date": "2026-01-01",
        "diameter_min_km": 0.01,
        "diameter_max_km": 0.02,
        "velocity_km_s": 5.0,
        "miss_distance_km": 50000000.0
    }
    
    # 2. Dados de um asteroide aparentemente perigoso (grande e perto)
    danger_asteroid = {
        "id": "67890",
        "name": "Doom Bringer",
        "date": "2026-01-01",
        "diameter_min_km": 2.5,
        "diameter_max_km": 3.5,
        "velocity_km_s": 25.0,
        "miss_distance_km": 500000.0
    }

    # 3. Dados inválidos para testar tratamento de erro
    invalid_asteroid = {
        "id": "999",
        "diameter_min_km": 0.5
        # Faltam campos obrigatórios
    }
    
    predictor = RiskPredictor()
    
    logger.info("--- Testando Asteroide Seguro (Expect: Low Risk) ---")
    res_safe = predictor.predict(safe_asteroid)
    print(f"Resultado Seguro: {res_safe}")
    
    logger.info("--- Testando Asteroide Perigoso (Expect: High Risk) ---")
    res_danger = predictor.predict(danger_asteroid)
    print(f"Resultado Perigoso: {res_danger}")
    
    logger.info("--- Testando Tratamento de Erro (Expect: ValueError) ---")
    try:
        predictor.predict(invalid_asteroid)
    except ValueError as e:
        logger.warning(f"Erro capturado com sucesso: {e}")
    
    # Testando com a função utilitária
    logger.info("--- Testando Função Utilitária ---")
    res_util = predict_asteroid_risk(danger_asteroid)
    print(f"Resultado Utilitário: {res_util}")

if __name__ == "__main__":
    test_inference()
