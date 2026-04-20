import sys
from pathlib import Path

# Adicionar o diretório src ao path para permitir imports do pacote astrostudy
root_dir = Path(__file__).parent.parent
sys.path.append(str(root_dir / "src"))

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from astrostudy.modeling.predict import RiskPredictor
from loguru import logger
import sys
from pathlib import Path

# Configuração da página - Premium Design
st.set_page_config(
    page_title="AstroStudy | Radar de Risco Orbital",
    page_icon="☄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS Customizado para aparência Premium
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4a4a4a;
    }
    .feature-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #58a6ff;
    }
    .interpretation-card {
        background-color: #1c2128;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def get_predictor():
    return RiskPredictor()

@st.cache_data
def load_asteroid_data():
    """Carrega o dataset de asteroides processados."""
    try:
        df = pd.read_csv("data/processed/asteroids_features.csv")
        # Criar label amigável para o seletor
        df['selector_label'] = df['name'] + " (" + df['date'] + ")"
        return df
    except Exception as e:
        st.error(f"Erro ao carregar base de dados: {e}")
        return pd.DataFrame()

def get_interpretation(res):
    prob = res['probability']
    feat = res['features']
    
    if prob > 0.6:
        msg = "⚠️ **ALERTA DE RISCO ELEVADO**: "
        reasons = []
        if feat['log_diameter'] > -1: reasons.append("grande diâmetro")
        if feat['log_velocity'] > 1.2: reasons.append("alta velocidade relativa")
        if feat['log_miss_distance'] < 6.5: reasons.append("proximidade crítica à Terra")
        
        if reasons:
            msg += f"O risco elevado se deve principalmente ao(à) {', '.join(reasons)}."
        else:
            msg += "A combinação de fatores físicos indica uma alta probabilidade de perigo orbital."
        return msg, "https://images-assets.nasa.gov/image/GSFC_20171208_Archive_e000305/GSFC_20171208_Archive_e000305~thumb.jpg"
    
    elif prob > 0.15:
        return "🟡 **RISCO MODERADO**: O objeto apresenta características que exigem monitoramento, embora não haja ameaça imediata confirmada.", "https://images-assets.nasa.gov/image/PIA00271/PIA00271~thumb.jpg"
    
    else:
        return "✅ **RISCO BAIXO**: O objeto é considerado seguro devido à sua trajetória distante ou dimensões reduzidas.", "https://images-assets.nasa.gov/image/PIA00271/PIA00271~thumb.jpg"

def get_divergence_analysis(model_pred, nasa_label, res):
    """Gera uma explicação analítica para divergências entre o modelo e a NASA."""
    if model_pred == nasa_label:
        return None
    
    prob = res['probability']
    feat = res['features']
    
    if model_pred == 1 and nasa_label == 0:
        # Modelo mais cauteloso que a NASA
        reason = "O modelo demonstrou **maior sensibilidade** a fatores físicos contínuos. "
        if feat['astrorisk_score'] > -5:
            reason += "O elevado *AstroRisk Score* (energia vs proximidade) sensibilizou o modelo, mesmo que o objeto não atinja os critérios estritos de 'PHA' da NASA."
        elif feat['log_miss_distance'] < 6.8:
            reason += "A proximidade extrema foi o fator determinante para o alerta da IA."
        else:
            reason += "A combinação de velocidade e massa sugere um perigo potencial que ultrapassa os limiares conservadores."
        return reason

    elif model_pred == 0 and nasa_label == 1:
        # NASA mais cautelosa que o Modelo
        reason = "O modelo foi **mais conservador** que a NASA neste caso. "
        if feat['log_diameter'] < -0.8:
            reason += "O diâmetro reduzido levou o modelo a classificar como seguro, enquanto a NASA pode estar considerando variáveis orbitais complexas ou incertezas que o baseline atual ainda não capturou plenamente."
        else:
            reason += "Isso pode indicar que o modelo atual exige uma combinação mais agressiva de fatores para disparar o alerta de risco."
        return reason
    
    return None

def main():
    # HEADER
    st.title("☄️ AstroStudy — Risk Analysis Dashboard")
    st.markdown("---")

    # SIDEBAR - CONFIG E INPUTS
    st.sidebar.image("https://www.nasa.gov/wp-content/themes/nasa/assets/images/nasa-logo.svg", width=100)
    st.sidebar.header("🕹️ Modo de Operação")
    
    mode = st.sidebar.radio(
        "Selecione a fonte de dados:",
        ["Simulação Manual", "Dados Reais (NASA Dataset)"]
    )
    
    st.sidebar.markdown("---")
    
    # Variáveis de entrada padrão
    d_min, d_max, velocity, miss_dist = 0.15, 0.35, 12.5, 25000000.0
    selected_asteroid_info = None

    if mode == "Dados Reais (NASA Dataset)":
        df_real = load_asteroid_data()
        if not df_real.empty:
            st.sidebar.subheader("🔍 Selecionar Asteroide")
            selected_label = st.sidebar.selectbox(
                "Escolha um registro da base:",
                df_real['selector_label'].unique()
            )
            
            # Extrair dados do asteroide selecionado
            row = df_real[df_real['selector_label'] == selected_label].iloc[0]
            d_min = float(row['diameter_min_km'])
            d_max = float(row['diameter_max_km'])
            velocity = float(row['velocity_km_s'])
            miss_dist = float(row['miss_distance_km'])
            selected_asteroid_info = row
            
            st.sidebar.success(f"Dados carregados para: {row['name']}")
        else:
            st.sidebar.warning("Base de dados real não encontrada.")

    st.sidebar.header("🛸 Parâmetros do Objeto")
    with st.sidebar:
        # Se for modo manual, os sliders funcionam normalmente. 
        # Se for real, eles mostram os valores mas ficam desabilitados ou apenas informativos
        d_min = st.slider("Diâmetro Mínimo (km)", 0.0, 5.0, d_min, 0.01, disabled=(mode != "Simulação Manual"))
        d_max = st.slider("Diâmetro Máximo (km)", 0.0, 5.0, d_max, 0.01, disabled=(mode != "Simulação Manual"))
        velocity = st.number_input("Velocidade Relativa (km/s)", 0.0, 50.0, velocity, disabled=(mode != "Simulação Manual"))
        miss_dist = st.number_input("Distância de Aproximação (km)", 0.0, 100000000.0, miss_dist, disabled=(mode != "Simulação Manual"))
        
        st.sidebar.markdown("---")
        if st.button("Resetar Parâmetros"):
            st.rerun()

    # ENGINE
    predictor = get_predictor()
    input_data = {
        "diameter_min_km": d_min,
        "diameter_max_km": d_max,
        "velocity_km_s": velocity,
        "miss_distance_km": miss_dist
    }
    
    try:
        res = predictor.predict(input_data)
        
        # Se tiver info real, mostrar cabeçalho do objeto
        if selected_asteroid_info is not None:
            st.info(f"### 🛰️ Analisando Objeto Real: **{selected_asteroid_info['name']}**")
            cols_info = st.columns(3)
            cols_info[0].metric("ID NASA", selected_asteroid_info['id'])
            cols_info[1].metric("Data de Aproximação", selected_asteroid_info['date'])
            nasa_hazardous = bool(selected_asteroid_info['is_hazardous'])
            cols_info[2].metric("Hazardous (NASA Label)", "Sim" if nasa_hazardous else "Não")
            
            # ANÁLISE DE DIVERGÊNCIA
            divergence_msg = get_divergence_analysis(res['prediction'], int(nasa_hazardous), res)
            if divergence_msg:
                st.warning("### 🔍 Análise de Divergência")
                st.markdown(f"""
                <div style="background-color: #2c1a1a; padding: 15px; border-radius: 10px; border-left: 5px solid #f85149;">
                    <strong>Observação Técnica:</strong> {divergence_msg}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.success("✅ **Consenso:** A predição da IA está em total acordo com a classificação oficial da NASA.")

        # LAYOUT PRINCIPAL
        col_res, col_viz = st.columns([1, 1])
        
        with col_res:
            st.subheader("🎯 Resultado da Predição AI")
            
            # Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = res['probability'] * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Probabilidade de Risco (%)", 'font': {'size': 24}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': "#58a6ff"},
                    'bgcolor': "white",
                    'borderwidth': 2,
                    'bordercolor': "gray",
                    'steps': [
                        {'range': [0, 15], 'color': '#238636'},
                        {'range': [15, 60], 'color': '#d29922'},
                        {'range': [60, 100], 'color': '#f85149'}
                    ],
                    'threshold': {
                        'line': {'color': "white", 'width': 4},
                        'thickness': 0.75,
                        'value': res['probability'] * 100
                    }
                }
            ))
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Arial"})
            st.plotly_chart(fig, use_container_width=True)
            
            status_color = "red" if res['is_hazardous'] else "green"
            st.markdown(f"### Classificação: <span style='color:{status_color}'>{res['risk_level']}</span>", unsafe_allow_html=True)

        with col_viz:
            st.subheader("🖼️ Visualização Contextual")
            interp_text, img_url = get_interpretation(res)
            st.image(img_url, caption="Representação artística do cenário orbital", use_container_width=True)
            
            st.markdown(f"""
            <div class="interpretation-card">
                <h4>🧠 Interpretação do Modelo</h4>
                <p style='font-size: 1.1em;'>{interp_text}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # FEATURE VIEW
        st.subheader("🛠️ Engenharia de Features (Deep Dive)")
        f_cols = st.columns(4)
        
        features = res['features']
        feat_info = {
            "log_diameter": ("Log Diâmetro", "Normaliza a escala exponencial do volume."),
            "log_velocity": ("Log Velocidade", "Destaca a ordem de magnitude da energia."),
            "log_miss_distance": ("Log Distância", "Escala a proximidade relativa."),
            "astrorisk_score": ("AstroRisk Score", "Aproximação da Energia Cinética Potencial.")
        }
        
        for i, (key, (label, desc)) in enumerate(feat_info.items()):
            with f_cols[i]:
                st.markdown(f"""
                <div class="feature-card">
                    <small>{label}</small>
                    <h3>{features[key]:.4f}</h3>
                    <p style='font-size: 0.8em; color: #8b949e;'>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        # HISTÓRICO ORBITAL (Diferencial Temporal)
        if selected_asteroid_info is not None:
            st.markdown("---")
            st.subheader("📈 Histórico de Aproximações Orbitais")
            
            # Filtrar todos os eventos deste mesmo asteroide pelo ID NASA
            asteroid_id = selected_asteroid_info['id']
            df_hist = load_asteroid_data()
            df_hist = df_hist[df_hist['id'] == asteroid_id].sort_values('date')
            
            num_passes = len(df_hist)
            st.write(f"🔍 **Insight Temporal:** Este objeto ({selected_asteroid_info['name']}) já registrou **{num_passes}** passagens próximas à Terra monitoradas neste dataset.")
            
            # Gráfico de Linha do Histórico
            col_h1, col_h2 = st.columns([2, 1])
            
            with col_h1:
                # Plotly Line Chart
                fig_hist = go.Figure()
                
                # Linha de Distância
                fig_hist.add_trace(go.Scatter(
                    x=df_hist['date'], 
                    y=df_hist['miss_distance_km'],
                    mode='lines+markers',
                    name='Distância (km)',
                    line=dict(color='#58a6ff', width=3),
                    marker=dict(size=8)
                ))
                
                fig_hist.update_layout(
                    title="Trajetória de Aproximação (Distância ao longo do tempo)",
                    xaxis_title="Data do Evento",
                    yaxis_title="Distância (km)",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "white"},
                    hovermode="x unified"
                )
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col_h2:
                # Mini-tabela de histórico
                st.markdown("**Resumo de Passagens:**")
                st.dataframe(
                    df_hist[['date', 'velocity_km_s', 'astrorisk_score']].rename(columns={
                        'date': 'Data',
                        'velocity_km_s': 'Vel. (km/s)',
                        'astrorisk_score': 'Score'
                    }), 
                    hide_index=True
                )

        # GUIA DO ESPECIALISTA
        st.markdown("---")
        with st.expander("📚 Guia do Especialista: Como entender esses números?"):
            st.markdown("""
            ### 1. Por que o tamanho importa?
            O diâmetro define a **massa** do asteroide. Objetos maiores não apenas causam mais impacto, mas têm mais chances de sobreviver à entrada na atmosfera terrestre.
            
            ### 2. A Velocidade é silenciosa e mortal
            A energia de um impacto depende do quadrado da velocidade. Se um asteroide dobra de velocidade, seu poder de destruição **quadruplica**.
            
            ### 3. O que é o AstroRisk Score?
            É uma fórmula exclusiva que criamos para aproximar a **Energia Cinética** do objeto em relação à sua **Proximidade**. 
            *   **Score Alto:** Muita energia e pouca distância.
            *   **Score Baixo:** Pouca energia ou muita distância.
            
            ### 4. Distância de Aproximação (Miss Distance)
            Embora 1 milhão de km pareça muito, no espaço isso é considerado "perto". O modelo monitora se essa distância é pequena o suficiente para que pequenas variações orbitais se tornem perigosas.
            """)

    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")

    # FOOTER
    st.markdown("---")
    st.caption("AstroStudy v1.1 | Desenvolvido para Análise Preditiva de Defesa Planetária")

if __name__ == "__main__":
    main()
