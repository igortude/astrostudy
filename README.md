---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![NASA API](https://img.shields.io/badge/NASA_API-0B3D91?style=for-the-badge&logo=nasa&logoColor=white)

---

## 💡 Resumo do projeto
O **AstroStudy** é uma solução avançada de Data Science e Engenharia de Dados desenvolvida para analisar e prever o risco de asteroides próximos à Terra (Near-Earth Objects). O sistema consome dados reais da **API NeoWs da NASA**, processa as variáveis astronômicas e utiliza **Machine Learning** para identificar ameaças iminentes.

O projeto evoluiu de um pipeline de processamento bruto para uma plataforma completa de monitoramento orbital, unindo rigor estatístico de nível sênior a uma interface interativa de alta performance.

---

## ❓ Problema de negócio / contexto
Agências espaciais frequentemente utilizam heurísticas booleanas rígidas (ex: *diâmetro > 150m* E *distância < 0.05 UA*) para rotular um asteroide como potencialmente perigoso. Treinar modelos de IA em cima dessas regras simples apenas cria algoritmos que decoram as regras humanas, sem aprender a verdadeira dinâmica física do risco.

**O desafio:** 
- Fugir do label fraco da NASA e criar uma variável de risco contínua e baseada em física.
- Lidar com um **desbalanceamento severo de classes** (cerca de 92% dos objetos são inofensivos).
- Minimizar Falsos Negativos a zero. Em Defesa Planetária, o custo de ignorar um asteroide perigoso é incalculável.

---

## 🛰️ Radar de Risco Orbital (Dashboard)
A jóia da coroa do projeto é o **Dashboard Interativo**, desenvolvido para ser uma ferramenta de análise profissional:

- **Modos de Operação Duplos**: Alterne entre **Simulação Manual** (para cenários "What-if") e **Dados Reais** (explorando o histórico da NASA).
- **IA Explicável (XAI)**: O sistema não apenas dá um "0 ou 1", mas explica *por que* um objeto é perigoso através do **AstroRisk Score**.
- **Análise de Divergência**: Uma funcionalidade avançada que detecta e explica discrepâncias entre a IA do projeto e a classificação oficial da NASA.
- **Histórico Temporal**: Visualize a biografia orbital de asteroides recorrentes através de gráficos de séries temporais.

---

## 📊 Dados e Metodologia
Os dados são extraídos automaticamente via pipeline customizado da API NeoWs da NASA.

### Arquitetura do Sistema:
1.  **Ingestão Resiliente**: Scripts com política de *Retry* e backoff exponencial.
2.  **Feature Engineering Física**: 
    *   **AstroRisk Score**: Aproximação de Energia Cinética ($E \propto d^3 \cdot v^2 / dist$).
    *   **Transformações Logarítmicas**: Estabilização de variância para modelos lineares.
3.  **Camada de Inferência (Production Ready)**: Classe `RiskPredictor` robusta, com validação de entrada e tratamento de erros profissional.

---

## 📈 Resultados (Data Case)
- **Recuperação (Recall) de 100%**: O modelo prioriza a segurança planetária, garantindo que **nenhuma ameaça real passe despercebida**, mesmo que isso gere alarmes falsos controlados.
- **Consistência Estatística**: Validado via *StratifiedKFold* com recall médio estável em 1.0000.

---

### 🛠️ Instalação e Execução

1. **Setup do Ambiente**:
   ```bash
   git clone https://github.com/igortude/AstroStudy.git
   cd AstroStudy
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   pip install -r requirements.txt # Ou instale manual: streamlit plotly pandas scikit-learn loguru joblib
   ```

2. **Executar o Dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```

3. **Pipelines de Dados (Opcional)**:
   ```bash
   python pipelines/run_ingestion.py   # Ingestão Raw
   python pipelines/run_processing.py  # Feature Engineering
   python pipelines/run_baseline_training.py # Treinamento do Modelo
   ```

---

Desenvolvido por **Igor** – *Cientista de Dados & Engenheiro de Machine Learning*

- [Portfólio Pessoal](https://github.com/igortude)
- [LinkedIn](https://www.linkedin.com/in/igor-tude-309480299/)
- [E-mail](mailto:igortude@hotmail.com)

---
*Este projeto é uma prova técnica de ponta a ponta, unindo Engenharia de Dados, Feature Engineering e Machine Learning aplicados.*
