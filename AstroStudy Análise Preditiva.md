# 🚀 AstroStudy — Análise Preditiva de Asteroides com Dados da NASA

O **AstroStudy** é um projeto de Ciência de Dados que utiliza dados reais da API NeoWs da NASA para analisar e prever o risco de asteroides próximos à Terra.

O projeto vai além de classificações simples, focando em **engenharia de features baseada em princípios físicos** e **decisões de modelagem orientadas ao risco real**.

---

## 🎯 Objetivo

Desenvolver um modelo capaz de identificar asteroides potencialmente perigosos, priorizando a **detecção de eventos críticos (alto recall)**, mesmo com aumento de falsos positivos.

---

## 🧠 Problema

A classificação padrão da NASA (`is_potentially_hazardous_asteroid`) é baseada em regras fixas, como:

- Diâmetro estimado
- Distância mínima da órbita terrestre

Isso limita a capacidade de análise mais profunda.

👉 Neste projeto, foi criada uma abordagem alternativa baseada em:

- Dinâmica física
- Relação entre tamanho, velocidade e distância
- Engenharia de variáveis contínuas

---

## 🔄 Pipeline do Projeto

1. Coleta de dados da API NeoWs (NASA)
2. Armazenamento em JSON (camada raw)
3. Processamento e limpeza dos dados
4. Engenharia de features
5. Treinamento de modelo preditivo
6. Avaliação com métricas adequadas ao problema

---

## ⚙️ Engenharia de Features

As principais transformações aplicadas foram:

### 🔹 Média Geométrica do Diâmetro
Combina os valores mínimo e máximo para reduzir ruído e redundância.

### 🔹 Transformação Logarítmica
Aplicada em variáveis físicas para:
- reduzir escala
- tratar outliers
- melhorar estabilidade do modelo

### 🔹 AstroRisk Score
Feature derivada baseada na relação:

- tamanho (volume ∝ d³)
- velocidade (energia ∝ v²)
- distância (inversamente proporcional ao risco)

### 🔹 Uncertainty Ratio
Mede a incerteza da estimativa do diâmetro.

---

## 🤖 Modelagem

### Modelo utilizado:
- Regressão Logística (baseline interpretável)

### Estratégias aplicadas:

- `class_weight="balanced"` para lidar com desbalanceamento
- Ajuste e análise de threshold
- Avaliação com foco em recall

---

## 📊 Resultados

| Métrica   | Resultado |
|----------|----------|
| Recall   | 100%     |
| Precision| ~40%     |
| F1-Score | ~0.57    |

---

## 🧠 Interpretação

O modelo foi ajustado para:

✔ Detectar todos os asteroides perigosos (Recall alto)  
⚠️ Aceitar maior número de falsos positivos  

👉 Essa escolha reflete o contexto do problema, onde **não detectar um risco é mais grave do que gerar um alarme falso**.

---

## ⚖️ Trade-off

Existe uma relação direta entre:

- Recall (detecção)
- Precision (confiabilidade)

O projeto prioriza **recall**, alinhado a cenários críticos como:

- detecção de fraudes  
- diagnósticos médicos  
- sistemas de alerta  

---

## ⚠️ Limitações

- Volume de dados reduzido (janela temporal curta)
- Poucos exemplos da classe minoritária (asteroides perigosos)
- Possível instabilidade nas métricas
- Necessidade de validação com dados históricos maiores

👉 O modelo ainda está em fase exploratória.

---

## 🚀 Próximos Passos

- Expandir o dataset (1+ ano de dados)
- Aplicar validação cruzada (cross-validation)
- Testar modelos mais robustos (Random Forest, XGBoost)
- Analisar curvas ROC e Precision-Recall
- Desenvolver dashboard interativo (Streamlit)

---

## 🧠 Insight Final

> Em problemas críticos, o melhor modelo não é o que mais acerta —  
> é o que menos erra quando o erro importa.

---

## 🛠️ Tecnologias

- Python
- Pandas / NumPy
- Scikit-learn
- Requests
- Streamlit (em desenvolvimento)

---

## 📌 Fonte de Dados

- NASA NeoWs API (Near Earth Object Web Service)

---

## 👨‍💻 Autor

Projeto desenvolvido como estudo prático de Ciência de Dados, com foco em:

- pensamento analítico  
- engenharia de features  
- tomada de decisão baseada em métricas  

---
