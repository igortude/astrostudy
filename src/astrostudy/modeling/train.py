import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix, precision_recall_curve
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import seaborn as sns
from loguru import logger
import joblib
from pathlib import Path

class ModelTrainer:
    """
    Treinador de modelos com foco em datasets desbalanceados e métricas de risco.
    """
    
    def __init__(self, random_state: int = 42, use_balanced_weights: bool = True):
        self.random_state = random_state
        # 1. CLASS WEIGHT BALANCED: Penaliza mais o erro na classe minoritária.
        # Fundamental para datasets onde o 'perigo' é raro.
        weights = "balanced" if use_balanced_weights else None
        self.model = LogisticRegression(
            random_state=self.random_state, 
            max_iter=1000,
            class_weight=weights
        )

    def prepare_data(self, df: pd.DataFrame, target_col: str, feature_cols: list[str]):
        X = df[feature_cols]
        y = df[target_col].astype(int)
        
        # Usamos stratify=y para garantir a mesma proporção de perigosos no treino e teste.
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.random_state, stratify=y
        )
        
        logger.info(f"Dados divididos: Treino={len(X_train)} | Teste={len(X_test)}")
        return X_train, X_test, y_train, y_test

    def train(self, X_train, y_train):
        logger.info(f"Treinando modelo (class_weight={self.model.class_weight})...")
        self.model.fit(X_train, y_train)
        logger.success("Treinamento concluído.")

    def evaluate_with_threshold(self, X_test, y_test, threshold: float = 0.5):
        """
        Avalia o modelo permitindo o ajuste do threshold de decisão.
        
        POR QUE: O padrão 0.5 é arbitrário. Em defesa planetária, preferimos 
        aceitar alguns alarmes falsos (Precision menor) do que deixar um 
        asteroide real passar (Recall maior).
        """
        # Obtém as probabilidades da classe 1 (Perigoso)
        y_probs = self.model.predict_proba(X_test)[:, 1]
        
        # Aplica o novo threshold
        y_pred = (y_probs >= threshold).astype(int)
        
        metrics = {
            "threshold": threshold,
            "accuracy": accuracy_score(y_test, y_pred),
            "precision": precision_score(y_test, y_pred, zero_division=0),
            "recall": recall_score(y_test, y_pred, zero_division=0),
            "f1": f1_score(y_test, y_pred, zero_division=0)
        }
        
        print(f"\n--- 📊 AVALIAÇÃO (THRESHOLD: {threshold}) ---")
        print(f"Acurácia:  {metrics['accuracy']:.4f}")
        print(f"Precisão:  {metrics['precision']:.4f}")
        print(f"Recall:    {metrics['recall']:.4f}")
        print(f"F1-Score:  {metrics['f1']:.4f}")
        
        print("\nMatriz de Confusão:")
        print(confusion_matrix(y_test, y_pred))
        
        return metrics

    def evaluate_cv(self, X: pd.DataFrame, y: pd.Series, cv: int = 5):
        """
        Executa validação cruzada estratificada para garantir consistência.
        
        POR QUE: Avaliar em múltiplos splits reduz o viés de uma única divisão 
        Treino/Teste, dando mais confiança nos resultados de Precision/Recall.
        """
        logger.info(f"Executando Cross-Validation (K-Fold estratificado, cv={cv})...")
        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=self.random_state)
        
        scoring = ['accuracy', 'precision', 'recall', 'f1']
        cv_results = cross_validate(self.model, X, y, cv=skf, scoring=scoring, n_jobs=-1)
        
        print("\n--- 📊 RELATÓRIO DE PERFORMANCE (CROSS-VALIDATION) ---")
        print(f"Acurácia Média: {cv_results['test_accuracy'].mean():.4f} (± {cv_results['test_accuracy'].std():.4f})")
        print(f"Precisão Média: {cv_results['test_precision'].mean():.4f} (± {cv_results['test_precision'].std():.4f})")
        print(f"Recall Médio:   {cv_results['test_recall'].mean():.4f} (± {cv_results['test_recall'].std():.4f})")
        print(f"F1-Score Médio: {cv_results['test_f1'].mean():.4f} (± {cv_results['test_f1'].std():.4f})")
        
        return cv_results

    def plot_precision_recall_curve(self, X_test, y_test, path: str = "models/reports/precision_recall_curve.png"):
        """
        Gera e salva o gráfico da curva Precision-Recall.
        
        POR QUE: Visualiza o trade-off contínuo entre Precision e Recall para 
        ajudar a escolher o melhor ponto de operação do modelo.
        """
        y_probs = self.model.predict_proba(X_test)[:, 1]
        precisions, recalls, thresholds = precision_recall_curve(y_test, y_probs)
        
        plt.figure(figsize=(10, 6))
        sns.set_theme(style="whitegrid")
        plt.plot(thresholds, precisions[:-1], "b--", label="Precision", linewidth=2)
        plt.plot(thresholds, recalls[:-1], "g-", label="Recall", linewidth=2)
        
        plt.xlabel("Threshold")
        plt.ylabel("Score")
        plt.title("Curva Precision-Recall vs Threshold")
        plt.legend(loc="best")
        
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(path)
        plt.close()
        logger.info(f"Curva Precision-Recall salva em {path}")

    def save_model(self, path: str = "models/trained/optimized_baseline.joblib"):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)
        logger.info(f"Modelo otimizado salvo em {path}")
