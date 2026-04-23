---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![NASA API](https://img.shields.io/badge/NASA_API-0B3D91?style=for-the-badge&logo=nasa&logoColor=white)

---

## 💡 Resumo do projeto
O **AstroStudy** é uma solução avançada de Data Science e Engenharia de Dados desenvolvida para analisar e prever o risco de asteroides próximos à Terra (Near-Earth Objects). O sistema consome dados reais da **API NeoWs da NASA**, processa as variáveis astronômicas e utiliza **Machine Learning** para identificar ameaças iminentes.

O diferencial deste projeto é o foco em **engenharia de features baseada em princípios físicos** e decisões de modelagem orientadas ao risco real, indo além de simples heurísticas booleanas.

---

## 🚀 Links
- 🔗 **Repositório:** [https://github.com/igortude/astrostudy](https://github.com/igortude/astrostudy)
- 🧪 **Demo Online:** [![Live Demo](https://img.shields.io/badge/Demo-Live-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://astrostudy-7eqypnocbcequa5w5wuerm.streamlit.app)


## 🧠 O Problema de Negócio (Data Science Case)
Agências espaciais frequentemente utilizam heurísticas rígidas (ex: *diâmetro > 150m* E *distância < 0.05 UA*) para rotular um asteroide. No entanto, o risco real é uma dinâmica contínua entre tamanho, velocidade e proximidade.

**Filosofia do Modelo:**
> "Em problemas críticos, o melhor modelo não é o que mais acerta — é o que menos erra quando o erro importa."

Para Defesa Planetária, o custo de um **Falso Negativo** (ignorar um meteoro perigoso) é infinito. Por isso, o AstroStudy foi otimizado para **Recall Máximo**, priorizando a detecção de todos os eventos críticos, mesmo aceitando um maior número de alarmes falsos (Falsos Positivos).

---

## 🛰️ Radar de Risco Orbital (Dashboard)
A ferramenta central é o **Dashboard Interativo**, que oferece:

- **Modos de Operação**: Alterne entre **Simulação Manual** e **Dados Reais** da NASA.
- **IA Explicável (XAI)**: Insights sobre o que influenciou a predição.
- **Análise de Divergência**: Detecta e explica por que a IA pode discordar da classificação oficial da NASA.
- **Histórico Temporal**: Rastreamento de múltiplas passagens de um mesmo asteroide.

---

## ⚙️ Engenharia de Features Sênior
- **Média Geométrica do Diâmetro**: Redução de ruído em medidas exponenciais.
- **Transformação Logarítmica**: Estabilização de outliers e normalização de escalas físicas.
- **AstroRisk Score**: Variável proprietária baseada na relação de **Energia Cinética** ($E \propto d^3 \cdot v^2 / dist$).
- **Uncertainty Ratio**: Métrica de incerteza da medição original da NASA.

---

## ⚖️ Nota de Humildade Técnica (Disclaimer)
Embora o AstroStudy utilize dados reais e técnicas avançadas de Machine Learning, este é um **projeto de natureza educacional e científica**. 

- **Autoridade**: A NASA e agências espaciais parceiras continuam sendo as fontes oficiais e definitivas para qualquer dado sobre Defesa Planetária.
- **Divergências**: Quando o modelo diverge da NASA, isso deve ser interpretado como uma diferença em **sensibilidade estatística** e critérios de threshold, e não como uma correção ao label institucional.
- **Finalidade**: O objetivo aqui é demonstrar o pipeline completo de Data Science e como diferentes métricas (como Recall vs Precision) impactam a tomada de decisão em cenários críticos.

---

## 📊 Resultados e Validação
| Métrica   | Resultado |
|----------|----------|
| **Recall (Sensibilidade)** | **100%** |
| **Precisão** | ~40% |
| **F1-Score** | ~0.57 |

O modelo foi validado via **Stratified Cross-Validation (5-folds)**, mantendo 100% de recall em todos os cenários, provando que a detecção é robusta e baseada em fundamentos físicos, não em sorte de split.

---

### 🛠️ Instalação e Execução

1. **Setup do Ambiente**:
   ```bash
   git clone https://github.com/igortude/AstroStudy.git
   cd AstroStudy
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   pip install -r requirements.txt
   ```

2. **Executar o Dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```

---

Desenvolvido por **Igor** – *Estudante de Ciência de Dados & Engenharia de Machine Learning*

- [Portfólio Pessoal](https://github.com/igortude)
- [LinkedIn](https://www.linkedin.com/in/igor-tude-309480299/)
- [E-mail](mailto:igortude@hotmail.com)

---
*Este projeto une Engenharia de Dados, Feature Engineering e Machine Learning em uma prova técnica de ponta a ponta.*
