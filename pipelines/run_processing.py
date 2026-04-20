from astrostudy.utils.logger import setup_logger
from astrostudy.processing.cleaner import DataCleaner
from astrostudy.features.engineer import FeatureEngineer
from loguru import logger
from pathlib import Path

def main():
    """
    Pipeline de Processamento: Raw -> Processed.
    Orquestra a limpeza e a engenharia de features.
    """
    setup_logger()
    logger.info("🛠️ Iniciando Pipeline de Processamento e Features")
    
    # 1. Limpeza e Flattening
    cleaner = DataCleaner()
    df_clean = cleaner.load_and_flatten()
    
    if df_clean.empty:
        logger.error("Nenhum dado encontrado para processar.")
        return

    # 2. Feature Engineering Sênior
    engineer = FeatureEngineer()
    df_final = engineer.engineer_features(df_clean)
    
    # 3. Persistência (Camada Processed)
    processed_dir = Path("data/processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    # Salvamos em CSV para fácil inspeção, mas em produção Parquet seria ideal.
    output_path = processed_dir / "asteroids_features.csv"
    df_final.to_csv(output_path, index=False)
    
    logger.success(f"✅ Processamento concluído! {len(df_final)} registros salvos em {output_path}")

if __name__ == "__main__":
    main()
