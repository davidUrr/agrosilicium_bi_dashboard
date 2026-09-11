# ui/styles.py
import streamlit as st

# Paleta de colores oficiales de Agrosilicium S.A.S.
HEX_VERDE_CORPORATIVO = "#2E7D32"  # Verde oscuro principal (representa agricultura y cultivos)
HEX_VERDE_FRESCO      = "#4CAF50"  # Verde secundario para acentos y botones interactivos
HEX_GRIS_FONDO        = "#F4F7F6"  # Fondo limpio y neutro para tarjetas y secciones secundarias
HEX_TEXTO_OSCURO      = "#1B3B2B"  # Tono oscuro con matiz verdoso para texto principal contrastado

def aplicar_estilos_corporativos():
    """Inyecta fuentes personalizadas y reglas CSS globales en la aplicación Streamlit."""
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700&family=Lato:wght@300;400;700&display=swap');
        
        .stSelectbox, .stMultiSelect, .stTextInput, div[data-baseweb="select"] {{
            font-family: 'Lato', sans-serif !important;
        }}
        
        .metric-box {{
            background-color: {HEX_GRIS_FONDO};
            padding: 22px;
            border-radius: 12px;
            border-top: 5px solid {HEX_VERDE_CORPORATIVO};
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s;
        }}
        .metric-box:hover {{
            transform: translateY(-2px);
            box-shadow: 0px 6px 15px rgba(15, 44, 89, 0.1);
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: #666666;
            font-weight: 600;
        }}
        .stTabs [aria-selected="true"] {{
            color: {HEX_VERDE_CORPORATIVO} !important;
            border-bottom-color: {HEX_VERDE_CORPORATIVO} !important;
        }}
        </style>
    """, unsafe_allow_html=True)