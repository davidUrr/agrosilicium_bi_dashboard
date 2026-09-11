# app_dashboard.py
import streamlit as st
from ui.styles import aplicar_estilos_corporativos
from ui.views.exportaciones import render_vista_exportaciones
from ui.views.importaciones import render_vista_importaciones
from ui.views.financiera import render_vista_financiera

# Configuración de Página
st.set_page_config(
    page_title="AGROSILICIUM MEJISULFATOS S.A.S.",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Aplicar branding y CSS global
aplicar_estilos_corporativos()

# Navegación Principal en Sidebar
with st.sidebar:
    st.image("logo.png", width=120)
    st.subheader("Inteligencia Aduanera")
    st.caption("AGROSILICIUM MEJISULFATOS S.A.S. — Suite Corporativa")
    st.divider()
    
    modulo_activo = st.radio(
        "Selecciona el Enfoque de Mercado:",
        [
            "Inteligencia de Exportaciones", 
            "Inteligencia de Importaciones", 
            "Inteligencia Financiera"
        ],
        key="modulo_master_selector"
    )
    st.divider()

# Enrutamiento hacia vistas modulares
if modulo_activo == "Inteligencia de Exportaciones":
    render_vista_exportaciones()
elif modulo_activo == "Inteligencia de Importaciones":
    render_vista_importaciones()
elif modulo_activo == "Inteligencia Financiera":
    render_vista_financiera()