import pandas as pd
from astrostudy.utils.logger import setup_logger
from astrostudy.modeling.train import ModelTrainer
from loguru import logger

def main():
    """
    Executa a comparação de thresholds para otimização de Recall.
    
    Este script demonstra o trade-off entre Precisão e Recall em um 
    problema de detecção de risco (asteroides).
    """
    setup_logger()
    logger.info("🤖 Iniciando Otimização de Threshold e Recall")
    
    # 1. Carregamento dos dados
    df = pd.read_csv("data/processed/asteroids_features.csv")
    features = ['log_diameter', 'log_velocity', 'log_miss_distance', 'astrorisk_score', 'uncertainty_ratio']
    target = 'is_hazardous'
    
    # 2. Treinamento com Class Weight 'Balanced'
    # POR QUE: Balanced ajusta os pesos inversamente proporcionais às frequências das classes.
    # Isso 'pune' o modelo mais severamente quando ele erra um asteroide perigoso.
    trainer = ModelTrainer(use_balanced_weights=True)
    X_train, X_test, y_train, y_test = trainer.prepare_data(df, target, features)
    trainer.train(X_train, y_train)
    
    # 3. Cross-Validation Estratificada
    # Avaliamos o modelo em toda a base usando 5 splits diferentes
    # para garantir que as métricas não são fruto de um "split de sorte".
    cv_results = trainer.evaluate_cv(df[features], df[target], cv=5)
    
    # 4. Treinamento Final e Gráficos
    # Treinamos no conjunto completo de treino para os gráficos
    trainer.train(X_train, y_train)
    
    # Geramos a Curva Precision-Recall
    trainer.plot_precision_recall_curve(X_test, y_test)
    
    # Mantemos a avaliação de thresholds só para logging rápido
    metrics = trainer.evaluate_with_threshold(X_test, y_test, threshold=0.5)

    
    # 5. Salvamento do Modelo Final
    trainer.save_model()
    logger.success("Experimento concluído e modelo salvo.")

if __name__ == "__main__":
    main()
