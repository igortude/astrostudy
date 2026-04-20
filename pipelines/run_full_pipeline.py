from astrostudy.utils.logger import setup_logger
from astrostudy.utils.config_loader import load_config
from astrostudy.ingestion.nasa_client import NASAClient
from astrostudy.processing.cleaner import DataCleaner
from astrostudy.features.engineer import FeatureEngineer
from astrostudy.modeling.train import ModelTrainer
from loguru import logger
import datetime

def main():
    # 1. Configuração Inicial
    setup_logger()
    config = load_config()
    
    # 2. Ingestão (Exemplo de data fixa)
    client = NASAClient()
    today = datetime.date.today().isoformat()
    raw_data = client.fetch_neo_feed(start_date=today, end_date=today)
    
    # 3. Processamento
    cleaner = DataCleaner()
    df_clean = cleaner.flatten_neo_data(raw_data)
    
    # 4. Feature Engineering
    engineer = FeatureEngineer()
    df_features = engineer.create_features(df_clean)
    
    # 5. Treinamento (Apenas se houver dados suficientes)
    if not df_features.empty:
        trainer = ModelTrainer(config)
        # Nota: Idealmente o treino usa dados históricos de data/processed/
        # Aqui é apenas uma demonstração do fluxo
        logger.info("Iniciando fluxo de treinamento demonstrativo")
        # trainer.train(df_features, target_col='is_potentially_hazardous')
        # trainer.save_model()
    else:
        logger.warning("Nenhum dado encontrado para processar.")

    logger.success("Pipeline executado com sucesso!")

if __name__ == "__main__":
    main()
