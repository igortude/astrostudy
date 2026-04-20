import streamlit as st
import pandas as pd
from astrostudy.utils.config_loader import load_config
from loguru import logger

# Configuração da página
st.set_page_config(
    page_title="AstroStudy - NASA Asteroid Risk Radar",
    page_icon="☄️",
    layout="wide"
)

def main():
    st.title("☄️ AstroStudy: Monitoramento de Asteroides")
    st.markdown("""
    Esta aplicação analisa dados da API **NASA NeoWs** para prever o risco de objetos próximos à Terra.
    """)
    
    # Sidebar
    st.sidebar.header("Configurações")
    config = load_config()
    
    # Layout em Colunas
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Visão Geral")
        st.info("O modelo está treinado para classificar asteroides como potencialmente perigosos.")
        
    with col2:
        st.subheader("🔍 Últimas Detecções")
        st.write("Dados em tempo real serão exibidos aqui.")

    # Placeholder para tabela de dados
    st.divider()
    st.subheader("Lista de Objetos")
    st.dataframe(pd.DataFrame(columns=["ID", "Nome", "Diâmetro (km)", "Velocidade (km/s)", "Risco"]))

if __name__ == "__main__":
    main()
