# ui/views/financiera.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db_utils import read_from_db
from ui.components import render_kpi_card
from ui.styles import HEX_VERDE_CORPORATIVO, HEX_VERDE_FRESCO

def resolver_columna(df, opciones):
    """Busca y retorna la primera coincidencia de nombre de columna existente en el DataFrame."""
    for col in opciones:
        if col in df.columns:
            return col
    return None

def render_vista_financiera():
    st.title("Inteligencia Financiera de Competidores")
    st.markdown("Análisis evolutivo de salud financiera y desempeño de los principales actores del mercado.")
    
    df_fin = read_from_db("financiero_competidores")
    
    if df_fin.empty:
        st.info("La tabla de datos financieros no está disponible en la base de datos.")
        return

    # Normalizar columna AÑO y filtrar desde 2020
    df_fin['AÑO'] = pd.to_numeric(df_fin['AÑO'], errors='coerce')
    df_fin = df_fin[df_fin['AÑO'] >= 2020]
    
    # Resolución dinámica de nombres de columnas (compatibilidad con minúsculas/mayúsculas/guiones bajos)
    col_ingresos = resolver_columna(df_fin, ['Ingresos netos por ventas', 'INGRESOS_NETOS_POR_VENTAS', 'Ingresos Netos Por Ventas', 'Total Ingreso Operativo'])
    col_utilidad = resolver_columna(df_fin, ['Ganancia (Pérdida) Neta', 'GANANCIA_NETA', 'Utilidad Neta', 'Ganancia Neta'])
    col_util_bruta = resolver_columna(df_fin, ['Utilidad bruta', 'UTILIDAD_BRUTA', 'Ganancia bruta'])
    col_ebit = resolver_columna(df_fin, ['Ganancia operativa (EBIT)', 'GANANCIA_OPERATIVA_EBIT', 'EBITDA'])
    
    col1, col2 = st.columns(2)
    with col1:
        empresas_disp = sorted(list(df_fin['EMPRESA'].dropna().unique()))
        empresa_sel = st.multiselect("Filtrar por Empresa:", empresas_disp, default=empresas_disp[:3] if empresas_disp else [])
    with col2:
        años_disp = sorted(list(df_fin['AÑO'].dropna().unique()), reverse=True)
        año_sel = st.multiselect("Filtrar por Año para KPIs:", años_disp, default=años_disp[:1] if años_disp else [])
        
    df_f = df_fin.copy()
    if empresa_sel: 
        df_f = df_f[df_f['EMPRESA'].isin(empresa_sel)]
    
    df_kpi = df_f[df_f['AÑO'].isin(año_sel)] if año_sel else df_f
        
    if df_f.empty:
        st.warning("No hay datos para los filtros seleccionados.")
        return

    # =========================================================================
    # MÉRTRICAS Y KPIS
    # =========================================================================
    k1, k2, k3, k4 = st.columns(4)
    
    ingresos_tot = df_kpi[col_ingresos].sum() if col_ingresos else 0
    utilidad_tot = df_kpi[col_utilidad].sum() if col_utilidad else 0
    margen_prom = (utilidad_tot / ingresos_tot * 100) if ingresos_tot != 0 else 0

    render_kpi_card(k1, "INGRESOS TOTALES (M-COP)", f"${ingresos_tot:,.0f}")
    render_kpi_card(k2, "UTILIDAD NETA TOTAL (M-COP)", f"${utilidad_tot:,.0f}")
    render_kpi_card(k3, "MARGEN NETO PROM.", f"{margen_prom:.2f}%")
    render_kpi_card(k4, "EMPRESAS EN ANÁLISIS", f"{df_f['EMPRESA'].nunique()}")

    st.write("")
    tab_f1, tab_f2, tab_f3 = st.tabs(["1. Tendencias Temporales", "2. Comparativa de Desempeño", "3. Detalle Financiero"])
    
    # --- PESTAÑA 1: TENDENCIAS ---
    with tab_f1:
        st.subheader("Evolución de Ingresos y Utilidad (M-COP)")
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            if col_ingresos:
                fig_trend_ing = px.line(
                    df_f.sort_values('AÑO'), x='AÑO', y=col_ingresos, color='EMPRESA', 
                    title="Tendencia de Ingresos Netos", markers=True, template="plotly_white"
                )
                st.plotly_chart(fig_trend_ing, use_container_width=True)
            else:
                st.info("Indicador de Ingresos no encontrado.")
                
        with col_t2:
            if col_utilidad:
                fig_trend_util = px.line(
                    df_f.sort_values('AÑO'), x='AÑO', y=col_utilidad, color='EMPRESA', 
                    title="Tendencia de Utilidad Neta", markers=True, template="plotly_white"
                )
                st.plotly_chart(fig_trend_util, use_container_width=True)
            else:
                st.info("Indicador de Utilidad Neta no encontrado.")

        # Evolución de Margen (%)
        if col_ingresos and col_utilidad:
            st.subheader("Evolución del Margen Neto (%)")
            df_trend = df_f.sort_values('AÑO').copy()
            df_trend['MARGEN_CALCULADO'] = (df_trend[col_utilidad] / df_trend[col_ingresos] * 100).fillna(0)
            
            fig_trend_margen = px.line(
                df_trend, x='AÑO', y='MARGEN_CALCULADO', color='EMPRESA',
                title="Evolución del Margen de Rentabilidad (%)", markers=True, template="plotly_white"
            )
            st.plotly_chart(fig_trend_margen, use_container_width=True)

    # --- PESTAÑA 2: COMPARATIVA ---
    with tab_f2:
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            if col_ingresos:
                fig_ing = px.bar(
                    df_kpi.sort_values(col_ingresos, ascending=False), 
                    x='EMPRESA', y=col_ingresos, 
                    title=f"Ingresos por Empresa - {año_sel if año_sel else 'Todos los años'}", 
                    color_discrete_sequence=[HEX_VERDE_CORPORATIVO], template="plotly_white"
                )
                st.plotly_chart(fig_ing, use_container_width=True)
                
        with col_chart2:
            if col_utilidad:
                fig_util = px.bar(
                    df_kpi.sort_values(col_utilidad, ascending=False), 
                    x='EMPRESA', y=col_utilidad, 
                    title=f"Utilidad Neta por Empresa - {año_sel if año_sel else 'Todos los años'}", 
                    color_discrete_sequence=[HEX_VERDE_FRESCO], template="plotly_white"
                )
                st.plotly_chart(fig_util, use_container_width=True)

    # --- PESTAÑA 3: MATRIZ DE DETALLE ---
    with tab_f3:
        st.subheader("Matriz de Indicadores Financieros Completos")
        cols_clave = ['EMPRESA', 'AÑO']
        for col_i in [col_ingresos, col_util_bruta, col_utilidad, col_ebit]:
            if col_i and col_i not in cols_clave:
                cols_clave.append(col_i)
                
        cols_finales = [c for c in cols_clave if c in df_f.columns]
        
        # Formato limpio con comas para la tabla
        format_dict = {col: '{:,.0f}' for col in cols_finales if col not in ['EMPRESA', 'AÑO']}
        st.dataframe(
            df_f[cols_finales].sort_values(['EMPRESA', 'AÑO'], ascending=[True, False]).style.format(format_dict), 
            use_container_width=True
        )