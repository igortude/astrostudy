---

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NASA API](https://img.shields.io/badge/NASA_API-0B3D91?style=for-the-badge&logo=nasa&logoColor=white)

---

## 💡 Resumo do projeto
O **AstroStudy** é uma solução avançada de Data Science e Engenharia de Dados desenvolvida para analisar e prever o risco de asteroides próximos à Terra (Near-Earth Objects). O sistema consome dados reais da **API NeoWs da NASA**, processa as variáveis astronômicas e utiliza **Machine Learning** para identificar ameaças iminentes.

O projeto transforma telemetria bruta espacial em inteligência preditiva, focando na segurança planetária e na eliminação de falsos negativos através de rigor estatístico de nível sênior.

---

## ❓ Problema de negócio / contexto
Agências espaciais frequentemente utilizam heurísticas booleanas rígidas (ex: *diâmetro > 150m* E *distância < 0.05 UA*) para rotular um asteroide como potencialmente perigoso. Treinar modelos de IA em cima dessas regras simples apenas cria algoritmos que decoram as regras humanas, sem aprender a verdadeira dinâmica física do risco.

**O desafio:** 
- Fugir do label fraco da NASA e criar uma variável de risco contínua e baseada em física.
- Lidar com um **desbalanceamento severo de classes** (cerca de 92% dos objetos são inofensivos).
- Minimizar Falsos Negativos a zero. Em Defesa Planetária, o custo de ignorar um asteroide perigoso é incalculável. Preferimos lidar com alarmes falsos (Falsos Positivos) do que ignorar ameaças.

---

## 📊 Dados utilizados
Os dados são extraídos automaticamente via pipeline customizado da API NeoWs da NASA (endpoint `/feed`), e armazenados em formato raw (JSON) para garantir imutabilidade:

| Feature | Descrição |
|--------|-----------|
| `estimated_diameter` | Diâmetros mínimo e máximo estimados (em km). |
| `relative_velocity` | Velocidade de aproximação do objeto (em km/s). |
| `miss_distance` | Distância do objeto em relação à Terra no ponto mais próximo. |
| `is_hazardous` | O label determinístico original da NASA (Alvo da modelagem base). |

> [!NOTE]
> O pipeline de ingestão (`DataSaver`) salva os dados em um envelope de metadados, garantindo a rastreabilidade, contagem de registros e idempotência das extrações diárias.

---

## 🛠️ Metodologia e ferramentas
A solução foi arquitetada em três camadas profissionais:

1.  **Engenharia de Dados (Ingestão)**: Scripts resilientes que executam chamadas à API da NASA em modo "chunked" (janelas de 7 dias) com políticas de *Retry* (Backoff Exponencial) para evitar limites de taxa (Rate Limits).
2.  **Feature Engineering Sênior (Inteligência Física)**: 
    *   Criação do **AstroRisk Score**, uma aproximação baseada em Energia Cinética ($E \propto d^3 \cdot v^2 / dist$).
    *   Aplicação de Transformações Logarítmicas ($log_{10}$) para estabilizar grandezas de diferentes ordens de magnitude.
3.  **Machine Learning (Foco em Risco)**: Treinamento de uma Regressão Logística com `class_weight='balanced'` e aplicação de Validação Cruzada Estratificada (*StratifiedKFold*) em 5 cenários.

---

## 📈 Principais insights e resultados (Data Case)
Após a coleta extensiva e execução do modelo Baseline, os seguintes resultados provaram a tese do projeto:

- **AstroRisk Score**: A nova variável contínua obteve forte correlação com os padrões da NASA, provando que o modelo pode aprender o risco de forma autônoma sem decorar regras rígidas.
- **Métrica de Sobrevivência (Recall)**: Ao balancear os pesos da classe minoritária, o algoritmo saltou de 50% para **100% de Sensibilidade**. 
- **O Trade-off Consciente**: Atingimos 100% de Recall sacrificando a Precisão (que se estabilizou em ~40%). Isso resultou em zero Falsos Negativos, traduzido na prática como: *"Nenhuma ameaça planetária passou despercebida."*

> [!IMPORTANT]
> **Validação Robusta**: Em testes de Cross-Validation com 5 divisões distintas, o modelo manteve **1.0000 de Recall médio**, comprovando que a capacidade do modelo não é resultado de um 'split de sorte', mas de features físicas bem fundamentadas.

---

### Pré-requisitos
- Python 3.11+
- Uma chave de API da [NASA API Portal](https://api.nasa.gov/)

### Instalação e Execução
1. Clone o repositório e acesse a pasta.
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Instale o pacote e as dependências:
   ```bash
   pip install -e .
   pip install pandas scikit-learn matplotlib seaborn loguru joblib
   ```
4. Configure sua chave da API:
   ```bash
   cp .env.example .env
   # Adicione NASA_API_KEY no arquivo
   ```
5. Execute os pipelines na ordem:
   ```bash
   # Baixar dados brutos
   python pipelines/run_ingestion.py
   
   # Tratar dados e gerar features (AstroRisk)
   python pipelines/run_processing.py
   
   # Treinar modelo, aplicar CV e gerar Curva PR
   python pipelines/run_baseline_training.py
   ```

---

Desenvolvido por **Igor** – *Cientista de Dados & Engenheiro de Machine Learning*

- [Portfólio Pessoal](https://github.com/igortude)
- [LinkedIn](https://www.linkedin.com/in/igor-tude-309480299/)
- [E-mail](mailto:igortude@hotmail.com)

---
*Este projeto é uma prova técnica de ponta a ponta, unindo Engenharia de Dados, Feature Engineering e Machine Learning aplicados.*
