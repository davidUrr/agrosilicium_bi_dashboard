# ui/views/exportaciones.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_utils import read_from_db
from ui.components import (
    render_kpi_card, 
    render_grafico_pareto, 
    render_mapa_mundial, 
    render_matriz_priorizacion_nichos
)
from ui.styles import HEX_VERDE_CORPORATIVO, HEX_VERDE_FRESCO

def mapear_pais_plotly(nombre_pais):
    """
    Convierte nombres de países en español (y variaciones DIAN/Confecámaras)
    a su nombre estándar en inglés compatible con Plotly Choropleth (locationmode='country names').
    Soporta los 122 países registrados en las bases de Exportación e Importación.
    """
    if not nombre_pais or pd.isna(nombre_pais):
        return nombre_pais

    mapeo = {
        # --- A ---
        'AFGANISTAN': 'Afghanistan',
        'ALBANIA': 'Albania',
        'ALEMANIA': 'Germany',
        'ANDORRA': 'Andorra',
        'ANGOLA': 'Angola',
        'ANGUILA': 'Anguilla',
        'ANTIGUA Y BARBUDA': 'Antigua and Barbuda',
        'ARABIA SAUDITA': 'Saudi Arabia',
        'ARGELIA': 'Algeria',
        'ARGENTINA': 'Argentina',
        'ARMENIA': 'Armenia',
        'ARUBA': 'Aruba',
        'AUSTRALIA': 'Australia',
        'AUSTRIA': 'Austria',
        'AZERBAIJAN': 'Azerbaijan',
        'AZERBAIYAN': 'Azerbaijan',

        # --- B ---
        'BAHAMAS': 'Bahamas',
        'BARBADOS': 'Barbados',
        'BELGICA': 'Belgium',
        'BELICE': 'Belize',
        'BERMUDA': 'Bermuda',
        'BERMUDAS': 'Bermuda',
        'BOLIVIA': 'Bolivia',
        'BRASIL': 'Brazil',
        'BRUNEI DARUSSALAM': 'Brunei',
        'BULGARIA': 'Bulgaria',

        # --- C ---
        'CAMBOYA': 'Cambodia',
        'CAMERUN': 'Cameroon',
        'CANADA': 'Canada',
        'CHEQUIA': 'Czech Republic',
        'CHILE': 'Chile',
        'CHINA': 'China',
        'CHIPRE': 'Cyprus',
        'COLOMBIA': 'Colombia',
        'ZONA FRANCA COLOMBIA': 'Colombia',
        'CONGO REPUBLICA DEL': 'Republic of the Congo',
        'COREA (SUR) REPUBLICA DE': 'South Korea',
        'COREA DEL SUR': 'South Korea',
        'COSTA DE MARFIL': "Cote d'Ivoire",
        'COSTA RICA': 'Costa Rica',
        'COTE D’IVOIRE': "Cote d'Ivoire",
        'CROACIA': 'Croatia',
        'CUBA': 'Cuba',
        'CURAZAO': 'Curacao',

        # --- D ---
        'DINAMARCA': 'Denmark',

        # --- E ---
        'ECUADOR': 'Ecuador',
        'EGIPTO': 'Egypt',
        'EL SALVADOR': 'El Salvador',
        'EMIRATOS ARABES UNIDOS': 'United Arab Emirates',
        'ESLOVAQUIA': 'Slovakia',
        'ESLOVENIA': 'Slovenia',
        'ESPANA': 'Spain',
        'ESPAÑA': 'Spain',
        'ESTADO DE PALESTINA': 'Palestine',
        'ESTADOS UNIDOS': 'United States',
        'EE.UU.': 'United States',
        'EEUU': 'United States',
        'ESTONIA': 'Estonia',

        # --- F ---
        'FEDERACION DE RUSIA': 'Russia',
        'RUSIA': 'Russia',
        'FILIPINAS': 'Philippines',
        'FINLANDIA': 'Finland',
        'FRANCIA': 'France',

        # --- G ---
        'GABON': 'Gabon',
        'GEORGIA': 'Georgia',
        'GHANA': 'Ghana',
        'GRANADA': 'Grenada',
        'GRECIA': 'Greece',
        'GUADALUPE': 'Guadeloupe',
        'GUATEMALA': 'Guatemala',
        'GUAYANA FRANCESA': 'French Guiana',
        'GUINEA': 'Guinea',
        'GUINEA - BISSAU': 'Guinea-Bissau',
        'GUINEA ECUATORIAL': 'Equatorial Guinea',
        'GUINEA-BISSAU': 'Guinea-Bissau',
        'GUYANA': 'Guyana',

        # --- H ---
        'HAITI': 'Haiti',
        'HONDURAS': 'Honduras',
        'HONG KONG': 'Hong Kong',
        'HUNGRIA': 'Hungary',

        # --- I ---
        'INDIA': 'India',
        'INDONESIA': 'Indonesia',
        'IRAK': 'Iraq',
        'IRAQ': 'Iraq',
        'IRLANDA': 'Ireland',
        'IRLANDA (EIRE)': 'Ireland',
        'ISLAS MARSHALL': 'Marshall Islands',
        'MARSHALL, ISLAS': 'Marshall Islands',
        'ISLAS TURCAS Y CAICOS': 'Turks and Caicos Islands',
        'TURCAS Y CAICOS, ISLAS': 'Turks and Caicos Islands',
        'ISLAS VIRGENES BRITANICAS': 'British Virgin Islands',
        'VIRGENES ISLAS (BRITANICAS)': 'British Virgin Islands',
        'VIRGENES ISLAS (ESTADOS UNIDOS)': 'United States Virgin Islands',
        'ISRAEL': 'Israel',
        'ITALIA': 'Italy',

        # --- J ---
        'JAMAICA': 'Jamaica',
        'JAPON': 'Japan',

        # --- K ---
        'KAZAJSTAN': 'Kazakhstan',
        'KUWAIT': 'Kuwait',

        # --- L ---
        'LETONIA': 'Latvia',
        'LIBANO': 'Lebanon',
        'LIBERIA': 'Liberia',
        'LIECHTENSTEIN': 'Liechtenstein',
        'LITUANIA': 'Lithuania',
        'LUXEMBURGO': 'Luxembourg',

        # --- M ---
        'MACAO': 'Macau',
        'MACEDONIA DEL NORTE': 'North Macedonia',
        'MADAGASCAR': 'Madagascar',
        'MALASIA': 'Malaysia',
        'MALI': 'Mali',
        'MARTINICA': 'Martinique',
        'MEXICO': 'Mexico',
        'MOZAMBIQUE': 'Mozambique',

        # --- N ---
        'NICARAGUA': 'Nicaragua',
        'NIGERIA': 'Nigeria',
        'NORUEGA': 'Norway',
        'NUEVA CALEDONIA': 'New Caledonia',
        'NUEVA ZELANDA': 'New Zealand',

        # --- O ---
        'OMAN': 'Oman',

        # --- P ---
        'PAISES BAJOS': 'Netherlands',
        'PAKISTAN': 'Pakistan',
        'PALESTINA': 'Palestine',
        'PANAMA': 'Panama',
        'PARAGUAY': 'Paraguay',
        'PERU': 'Peru',
        'POLONIA': 'Poland',
        'PORTUGAL': 'Portugal',
        'PUERTO RICO': 'Puerto Rico',

        # --- Q ---
        'QATAR': 'Qatar',

        # --- R ---
        'REINO UNIDO': 'United Kingdom',
        'REPUBLICA CHECA': 'Czech Republic',
        'REPUBLICA DOMINICANA': 'Dominican Republic',
        'RUMANIA': 'Romania',

        # --- S ---
        'SAINT KITTS Y NEVIS': 'Saint Kitts and Nevis',
        'SAN CRISTOBAL Y NIEVES': 'Saint Kitts and Nevis',
        'SAN VICENTE Y LAS GRANADINAS': 'Saint Vincent and the Grenadines',
        'SANTA LUCIA': 'Saint Lucia',
        'SAMOA': 'Samoa',
        'SAN MARINO': 'San Marino',
        'SENEGAL': 'Senegal',
        'SERBIA': 'Serbia',
        'SIERRA LEONA': 'Sierra Leone',
        'SINGAPUR': 'Singapore',
        'SUDAFRICA': 'South Africa',
        'SUDAFRICA, REPUBLICA DE': 'South Africa',
        'SUECIA': 'Sweden',
        'SUIZA': 'Switzerland',
        'SURINAM': 'Suriname',

        # --- T ---
        'TAILANDIA': 'Thailand',
        'TAIWAN': 'Taiwan',
        'TANZANIA': 'Tanzania',
        'TANZANIA REP UNIDA DE': 'Tanzania',
        'TRINIDAD Y TABAGO': 'Trinidad and Tobago',
        'TRINIDAD Y TOBAGO': 'Trinidad and Tobago',
        'TUNEZ': 'Tunisia',
        'TURQUIA': 'Turkey',

        # --- U ---
        'UCRANIA': 'Ukraine',
        'UGANDA': 'Uganda',
        'URUGUAY': 'Uruguay',

        # --- V ---
        'VENEZUELA': 'Venezuela',
        'VIETNAM': 'Vietnam'
    }

    key = str(nombre_pais).strip().upper()
    return mapeo.get(key, nombre_pais)

def render_vista_exportaciones():
    st.title("Inteligencia Competitiva de Exportaciones")
    st.divider()

    # Carga de datasets
    datos_raw = read_from_db("expo_enriquecida")
    nichos_df = read_from_db("e02_top_exportadores")
    pareto_df = read_from_db("e04_pareto_exportacion")
    dispais_df = read_from_db("e05_dist_pais_expo")

    if datos_raw.empty:
        st.warning("No hay datos de exportaciones en la base de datos central.")
        return

    # Normalización de columnas en memoria
    col_pais = 'PAIS_DESTINO_FINAL' if 'PAIS_DESTINO_FINAL' in datos_raw.columns else 'PAIS_DESTINO'
    col_buyer = 'RAZON_SOCIAL_DESTINATARIO_NORMALIZADO' if 'RAZON_SOCIAL_DESTINATARIO_NORMALIZADO' in datos_raw.columns else 'RAZON_SOCIAL_DESTINATARIO'
    col_exp = 'NOMBRE_EXPORTADOR' if 'NOMBRE_EXPORTADOR' in datos_raw.columns else 'RAZON_SOCIAL_EXPORTADOR'

    # =========================================================================
    # 🔍 FILTROS REACTIVOS EN LA BARRA LATERAL (3 NIVELES)
    # =========================================================================
    st.sidebar.subheader("🔍 Filtros de Exportación")
    
    # 1. Filtro por Nicho
    opciones_nichos = sorted(list(datos_raw['NICHO'].dropna().unique()))
    nichos_sel = st.sidebar.multiselect("Filtrar por Nicho Económico:", opciones_nichos, key="n_exp")
    
    # 2. Filtro por Subpartida (Jerárquico)
    df_sub = datos_raw[datos_raw['NICHO'].isin(nichos_sel)] if nichos_sel else datos_raw
    col_sub_raw = 'SUBPARTIDA' if 'SUBPARTIDA' in df_sub.columns else 'SUBPARTIDA_ARANCELARIA'
    opciones_subs = sorted(list(df_sub[col_sub_raw].astype(str).dropna().unique()))
    subs_sel = st.sidebar.multiselect("Filtrar por Subpartida:", opciones_subs, key="s_exp")
    
    # 3. Filtro por País de Destino
    opciones_paises = sorted(list(datos_raw[col_pais].dropna().unique()))
    paises_sel = st.sidebar.multiselect("Filtrar por País de Destino:", opciones_paises, key="p_exp")

    # Función de filtrado dinámico aplicable a cualquier DataFrame
    def aplicar_filtros(df, col_n='NICHO', col_s=col_sub_raw, col_p=col_pais):
        res = df.copy()
        if nichos_sel and col_n in res.columns:
            res = res[res[col_n].isin(nichos_sel)]
        if subs_sel and col_s in res.columns:
            res = res[res[col_s].astype(str).isin(subs_sel)]
        if paises_sel:
            if col_p in res.columns:
                res = res[res[col_p].isin(paises_sel)]
            elif 'PRINCIPAL_PAIS_DESTINO' in res.columns:
                res = res[res['PRINCIPAL_PAIS_DESTINO'].isin(paises_sel)]
            elif 'PAIS_DESTINO' in res.columns:
                res = res[res['PAIS_DESTINO'].isin(paises_sel)]
        return res

    # DataFrames filtrados dinámicamente
    df_datos_f = aplicar_filtros(datos_raw)
    df_nichos_f = aplicar_filtros(nichos_df)
    df_pareto_f = aplicar_filtros(pareto_df)
    df_dispais_f = aplicar_filtros(dispais_df, col_p='PAIS_DESTINO')

    if df_datos_f.empty:
        st.warning("No hay datos para los filtros seleccionados.")
        return

    # =========================================================================
    # 🎯 SECCIÓN DE TOMA DE DECISIONES: MARKET SHARE DE AGROSILICIUM S.A.
    # =========================================================================
    fob_total = df_datos_f["VALOR_FOB_USD"].sum()
    df_extrusiones = df_datos_f[df_datos_f[col_exp].astype(str).str.contains("AGROSILICIUM", na=False)]
    fob_extrusiones = df_extrusiones["VALOR_FOB_USD"].sum()
    share_global = (fob_extrusiones / fob_total * 100) if fob_total > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    render_kpi_card(k1, "TOTAL EXPORTADO (FOB)", f"USD ${fob_total:,.2f}")
    render_kpi_card(k2, "VENTAS AGROSILICIUM S.A.S.", f"USD ${fob_extrusiones:,.2f}")
    render_kpi_card(k3, "MARKET SHARE PROPIO", f"{share_global:.2f}%")
    render_kpi_card(k4, "MERCADOS ACTIVADOS", f"{df_datos_f[col_pais].nunique()} Países")

    st.write("")

    # =========================================================================
    # 📑 PESTAÑAS ANALÍTICAS Y ESTRATÉGICAS
    # =========================================================================
    tab_est, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "1. Matriz Estratégica & Expansión",
        "2. Estructura de Mercado & Pareto", 
        "3. Ranking de Competidores", 
        "4. Distribución Geográfica", 
        "5. Clientes Internacionales", 
        "6. Perfil del Comprador", 
        "7. Perfil del Proveedor"
    ])

    # --- PESTAÑA ESTRATÉGICA: MATRIZ DE PRIORIZACIÓN Y TABLAS DE RECOMENDACIÓN ---
    with tab_est:
        st.subheader("Priorización de Nichos y Oportunidades de Expansión Internacional")
        if not pareto_df.empty:
            col_actores = 'NUM_ACTORES_UNICOS' if 'NUM_ACTORES_UNICOS' in pareto_df.columns else ('NUM_EXPORTADORES_UNICOS' if 'NUM_EXPORTADORES_UNICOS' in pareto_df.columns else 'NUM_TRANSACCIONES')
            df_matriz = pareto_df.groupby('NICHO').agg(
                VALOR_TOTAL_USD=('VALOR_TOTAL_USD' if 'VALOR_TOTAL_USD' in pareto_df.columns else 'VALOR_FOB_USD', 'sum'),
                NUM_COMPETIDORES=(col_actores, 'sum')
            ).reset_index()
            
            fig_matriz = render_matriz_priorizacion_nichos(df_matriz, 'NICHO', 'VALOR_TOTAL_USD', 'NUM_COMPETIDORES')
            st.plotly_chart(fig_matriz, use_container_width=True)

        st.divider()
        st.subheader("Panel de Recomendaciones & Desglose Estratégico")
        c_rec1, c_rec2, c_rec3, c_rec4 = st.columns(4)
        
        # 1. TARJETA Y TABLA DE NICHOS
        with c_rec1:
            st.markdown("##### 🟢 Nichos de Oportunidad")
            st.info("Priorizar nichos en el cuadrante de alto volumen USD y menor fragmentación de competencia.")
            df_t_nichos = df_datos_f.groupby('NICHO').agg(
                TAMAÑO_USD=('VALOR_FOB_USD', 'sum')
            ).reset_index().sort_values('TAMAÑO_USD', ascending=False)
            st.dataframe(
                df_t_nichos.style.format({'TAMAÑO_USD': '${:,.2f}'}).hide(axis='index'),
                use_container_width=True
            )
        
        # 2. TARJETA Y TABLA DE DIVERSIFICACIÓN GEOGRÁFICA
        with c_rec2:
            st.markdown("##### 🔵 Diversificación Geográfica")
            p_top = df_datos_f.groupby(col_pais)['VALOR_FOB_USD'].sum().sort_values(ascending=False).index[:3].tolist()
            st.success(f"Principales destinos: **{', '.join(p_top[:2])}**. Priorizar alianzas en estos mercados.")
            df_t_paises = df_datos_f.groupby(col_pais).agg(
                TAMAÑO_USD=('VALOR_FOB_USD', 'sum')
            ).reset_index().sort_values('TAMAÑO_USD', ascending=False)
            df_t_paises.rename(columns={col_pais: 'PAÍS DESTINO'}, inplace=True)
            st.dataframe(
                df_t_paises.style.format({'TAMAÑO_USD': '${:,.2f}'}).hide(axis='index'),
                use_container_width=True
            )

        # 3. TARJETA Y TABLA DE CLIENTES COMPETIDORES
        with c_rec3:
            st.markdown("##### 🟡 Clientes Competidores")
            top_comp_buyer = df_datos_f.groupby(col_buyer)['VALOR_FOB_USD'].sum().sort_values(ascending=False).index[0] if col_buyer in df_datos_f.columns else "N/A"
            st.warning(f"Comprador principal: **`{top_comp_buyer}`**. Analizar su portfolio de suministro.")
            df_t_clientes = df_datos_f.groupby(col_buyer).agg(
                TAMAÑO_USD=('VALOR_FOB_USD', 'sum')
            ).reset_index().sort_values('TAMAÑO_USD', ascending=False)
            df_t_clientes.rename(columns={col_buyer: 'CLIENTE CLAVE'}, inplace=True)
            st.dataframe(
                df_t_clientes.head(15).style.format({'TAMAÑO_USD': '${:,.2f}'}).hide(axis='index'),
                use_container_width=True
            )

        # 4. TARJETA Y TABLA DE SUBPARTIDAS (NUEVO ELEMENTO)
        with c_rec4:
            st.markdown("##### 🟣 Subpartidas Arancelarias")
            top_sub = df_datos_f.groupby(col_sub_raw)['VALOR_FOB_USD'].sum().sort_values(ascending=False).index[0] if col_sub_raw in df_datos_f.columns else "N/A"
            st.error(f"Subpartida líder: **`{top_sub}`**. Enfocar la capacidad de manufactura técnica.")
            df_t_subs = df_datos_f.groupby(col_sub_raw).agg(
                TAMAÑO_USD=('VALOR_FOB_USD', 'sum')
            ).reset_index().sort_values('TAMAÑO_USD', ascending=False)
            df_t_subs.rename(columns={col_sub_raw: 'SUBPARTIDA'}, inplace=True)
            st.dataframe(
                df_t_subs.head(15).style.format({'TAMAÑO_USD': '${:,.2f}'}).hide(axis='index'),
                use_container_width=True
            )

    # --- PESTAÑA 1: PARETO Y GRÁFICO DINÁMICO ---
    with tab1:
        st.subheader("Análisis de Pareto y Estructura de Exportación")
        col_s_p = 'SUBPARTIDA' if 'SUBPARTIDA' in df_pareto_f.columns else 'SUBPARTIDA_ARANCELARIA'
        
        if not nichos_sel and not subs_sel and not paises_sel:
            df_c = df_pareto_f.head(15).copy()
            df_c['ETIQUETA'] = df_c['NICHO'] + " (" + df_c[col_s_p].astype(str) + ")"
            val_col = 'VALOR_TOTAL_USD' if 'VALOR_TOTAL_USD' in df_c.columns else 'VALOR_FOB_USD'
            fig = render_grafico_pareto(df_c, 'ETIQUETA', val_col, 'PORCENTAJE_ACUMULADO')
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df_pareto_f.style.format({val_col: '${:,.2f}', 'PORCENTAJE_ACUMULADO': '{:.2f}%'}).hide(), use_container_width=True)
        else:
            # GRÁFICO COMPLEMENTARIO DINÁMICO AL FILTRAR
            st.caption("**Estructura Comercial Dinámica para la Selección Actual:**")
            col_grp = col_sub_raw if col_sub_raw in df_datos_f.columns else 'NICHO'
            df_bar_filt = df_datos_f.groupby([col_grp]).agg(TOTAL_FOB=('VALOR_FOB_USD', 'sum')).reset_index().sort_values('TOTAL_FOB', ascending=False).head(10)
            
            fig_sub_bar = px.bar(
                df_bar_filt, x='TOTAL_FOB', y=col_grp, orientation='h',
                title=f"Top Subpartidas / Segmentos Filtrados (USD FOB)",
                color_discrete_sequence=[HEX_VERDE_CORPORATIVO], template="plotly_white"
            )
            st.plotly_chart(fig_sub_bar, use_container_width=True)

            st.caption("**Tabla Detallada de Transacciones Filtradas:**")
            st.dataframe(df_datos_f.head(100).style.format({'VALOR_FOB_USD': '${:,.2f}'}), use_container_width=True)

    # --- PESTAÑA 2: RANKING COMPETIDORES ---
    with tab2:
        if len(df_nichos_f) > 0:
            df_top = df_nichos_f.sort_values('VALOR_FOB_USD', ascending=False).head(10)
            st.plotly_chart(px.bar(df_top, x='VALOR_FOB_USD', y='NOMBRE_EXPORTADOR', orientation='h', color_discrete_sequence=[HEX_VERDE_FRESCO], template="plotly_white"), use_container_width=True)
            b_comp = st.text_input("Buscar exportador local (Nombre o NIT):", key="b_exp_table")
            df_out = df_nichos_f.sort_values('RANKING_EN_NICHO')
            if b_comp:
                df_out = df_out[df_out['NOMBRE_EXPORTADOR'].astype(str).str.contains(b_comp.upper(), na=False) | df_out['NIT_EXPORTADOR'].astype(str).str.contains(b_comp, na=False)]
            st.dataframe(df_out.style.format({'VALOR_FOB_USD': '${:,.2f}', 'PORCENTAJE_DEL_MERCADO': '{:.2f}%'}).hide(), use_container_width=True)

    # --- PESTAÑA 3: DISTRIBUCIÓN GEOGRÁFICA Y MAPA MUNDIAL ---
    with tab3:
        if len(df_dispais_f) > 0:
            val_col = 'VALOR_USD' if 'VALOR_USD' in df_dispais_f.columns else 'VALOR_FOB_USD'
            g_p = df_dispais_f.groupby('PAIS_DESTINO').agg({val_col:'sum'}).reset_index().sort_values(val_col, ascending=False)
            
            # Mapeo de nombres de países para compatibilidad con Plotly Choropleth
            g_p['PAIS_PLOTLY'] = g_p['PAIS_DESTINO'].apply(mapear_pais_plotly)
            
            # Mapa Coroplético Mundial
            fig_mapa = render_mapa_mundial(g_p, 'PAIS_PLOTLY', val_col, "Mapa Mundial de Calor de Exportaciones por País Destino")
            st.plotly_chart(fig_mapa, use_container_width=True)
            
            # Alerta de Riesgo de Concentración
            top1_pais = g_p.iloc[0]['PAIS_DESTINO'] if not g_p.empty else "N/A"
            top1_val = g_p.iloc[0][val_col] if not g_p.empty else 0
            pct_concentracion = (top1_val / fob_total * 100) if fob_total > 0 else 0
            if pct_concentracion > 40:
                st.warning(f"⚠️ **Alerta de Concentración:** El **{pct_concentracion:.1f}%** de las exportaciones dependen de un solo país (`{top1_pais}`). Se recomienda diversificar hacia nuevos mercados.")

            st.plotly_chart(px.bar(g_p.head(12), x='PAIS_DESTINO', y=val_col, color_discrete_sequence=[HEX_VERDE_CORPORATIVO], template="plotly_white"), use_container_width=True)
            st.dataframe(df_dispais_f.style.format({val_col: '${:,.2f}'}).hide(), use_container_width=True)

    # --- PESTAÑA 4: CLIENTES INTERNACIONALES ---
    with tab4:
        if len(df_datos_f) > 0:
            df_cl = df_datos_f.groupby(['NICHO', 'SUBPARTIDA', col_buyer]).agg(
                VALOR_USD=('VALOR_FOB_USD', 'sum'), 
                NUM_TRANSACCIONES=('VALOR_FOB_USD', 'count')
            ).reset_index().sort_values('VALOR_USD', ascending=False)
            
            map_p = df_datos_f.groupby(col_buyer)[col_pais].agg(lambda x: x.mode()[0] if len(x.mode())>0 else x.iloc[0]).to_dict()
            df_cl['PAIS_DESTINO'] = df_cl[col_buyer].map(map_p).fillna("No Identificado")
            df_cl.rename(columns={col_buyer: 'COMPRADOR_INTERNACIONAL'}, inplace=True)
            
            total_fob_actual = df_cl['VALOR_USD'].sum()
            df_cl['VALOR_ACUMULADO_USD'] = df_cl['VALOR_USD'].cumsum().round(2)
            df_cl['PORCENTAJE'] = ((df_cl['VALOR_USD'] / total_fob_actual) * 100).round(2) if total_fob_actual > 0 else 0
            df_cl['PORCENTAJE_ACUMULADO'] = ((df_cl['VALOR_ACUMULADO_USD'] / total_fob_actual) * 100).round(2) if total_fob_actual > 0 else 0
            
            b_cli = st.text_input("Filtrar por Razón Social del Comprador:", key="b_cli_table")
            if b_cli: 
                df_cl = df_cl[df_cl['COMPRADOR_INTERNACIONAL'].astype(str).str.contains(b_cli.upper(), na=False)]
            st.dataframe(df_cl.style.format({'VALOR_USD': '${:,.2f}', 'VALOR_ACUMULADO_USD': '${:,.2f}', 'PORCENTAJE': '{:.2f}%', 'PORCENTAJE_ACUMULADO': '{:.2f}%'}).hide(), use_container_width=True)

    # --- PESTAÑA 5: PERFIL DEL COMPRADOR ---
    with tab5:
        st.subheader("Análisis de Suministro y Lealtad Comercial")
        if col_buyer in df_datos_f.columns:
            lista_c = sorted(list(df_datos_f[col_buyer].dropna().unique()))
            c_foco = st.selectbox("Selecciona un Comprador Internacional para auditar su cadena de suministro:", lista_c, key="f_c_exp")
            
            if c_foco:
                df_f = df_datos_f[df_datos_f[col_buyer] == c_foco]
                fob_total_cliente = df_f['VALOR_FOB_USD'].sum()
                
                st.markdown(f"**Ficha Técnica Comercial:** `{c_foco}`")
                sk1, sk2, sk3 = st.columns(3)
                render_kpi_card(sk1, "PRESUPUESTO CAPTURADO (FOB)", f"USD ${fob_total_cliente:,.2f}")
                render_kpi_card(sk2, "NÚMERO DE PEDIDOS", f"{len(df_f):,} Envíos")
                nit_col = 'NIT_EXPORTADOR' if 'NIT_EXPORTADOR' in df_f.columns else col_exp
                render_kpi_card(sk3, "EXPORTADORES QUE LE VENDEN", f"{df_f[nit_col].nunique()} Empresas")
                
                df_prov_share = df_f.groupby(col_exp).agg(VALOR_FOB_USD=('VALOR_FOB_USD', 'sum')).reset_index().sort_values('VALOR_FOB_USD', ascending=False)
                st.plotly_chart(px.pie(df_prov_share, values='VALOR_FOB_USD', names=col_exp, title="Share of Wallet (Suministro desde Colombia)", hole=0.4), use_container_width=True)
                
                st.divider()
                st.subheader("Detalle de Entregas y Proveedores Colombianos")
                df_detalle_prov = df_f.groupby(col_exp).agg(
                    VALOR_FOB_USD=('VALOR_FOB_USD', 'sum'),
                    NUM_TRANSACCIONES=('VALOR_FOB_USD', 'count')
                ).reset_index().sort_values('VALOR_FOB_USD', ascending=False)
                
                df_detalle_prov['PORCENTAJE_PARTICIPACION'] = (df_detalle_prov['VALOR_FOB_USD'] / fob_total_cliente * 100) if fob_total_cliente > 0 else 0
                df_detalle_prov.rename(columns={
                    col_exp: 'EXPORTADOR COLOMBIANO', 
                    'VALOR_FOB_USD': 'VALOR TOTAL (USD)', 
                    'NUM_TRANSACCIONES': 'CANTIDAD DE ENVÍOS', 
                    'PORCENTAJE_PARTICIPACION': '% PARTICIPACIÓN'
                }, inplace=True)
                
                st.dataframe(df_detalle_prov.style.format({
                    'VALOR TOTAL (USD)': '${:,.2f}', 
                    '% PARTICIPACIÓN': '{:.2f}%', 
                    'CANTIDAD DE ENVÍOS': '{:,}'
                }).hide(axis='index'), use_container_width=True)
                
                with st.expander("Ver histórico completo de despachos recibidos por este comprador"):
                    cols_despacho = [c for c in ['FECHA', 'FECHA_PROCESO', 'SUBPARTIDA', 'DESCRIPCION', col_exp, col_pais, 'VALOR_FOB_USD', 'KG_NETO'] if c in df_f.columns]
                    if cols_despacho:
                        st.dataframe(df_f[cols_despacho].style.format({'VALOR_FOB_USD': '${:,.2f}'}), use_container_width=True)
                    else:
                        st.dataframe(df_f.head(100), use_container_width=True)

    # --- PESTAÑA 6: PERFIL DEL PROVEEDOR (EXPORTADOR LOCAL) ---
    with tab6:
        st.subheader("Auditoría de Mercado del Exportador Local")
        if col_exp in df_datos_f.columns:
            lista_e = sorted(list(df_datos_f[col_exp].dropna().unique()))
            e_foco = st.selectbox("Selecciona un Exportador Local para auditar su mercado:", lista_e, key="f_e_exp")
            
            if e_foco:
                df_f = df_datos_f[df_datos_f[col_exp] == e_foco]
                fob_total_prov = df_f['VALOR_FOB_USD'].sum()
                st.markdown(f"**Ficha de Inteligencia:** `{e_foco}`")
                
                sub_p_kpi1, sub_p_kpi2, sub_p_kpi3 = st.columns(3)
                render_kpi_card(sub_p_kpi1, "MONTO EXPORTADO CAPTURADO", f"USD ${fob_total_prov:,.2f}")
                render_kpi_card(sub_p_kpi2, "DESPACHOS EFECTUADOS", f"{len(df_f):,} Envíos")
                render_kpi_card(sub_p_kpi3, "CARTERA DE CLIENTES ACTIVOS", f"{df_f[col_buyer].nunique() if col_buyer in df_f.columns else 0} Compradores")
                
                df_dist_paises_prov = df_f.groupby(col_pais).agg(VALOR_FOB_USD=('VALOR_FOB_USD', 'sum')).reset_index().sort_values(by='VALOR_FOB_USD', ascending=False)
                st.plotly_chart(px.bar(df_dist_paises_prov.head(10), x='VALOR_FOB_USD', y=col_pais, orientation='h', title="Top 10 Mercados Destino", color_discrete_sequence=[HEX_VERDE_CORPORATIVO]), use_container_width=True)
                
                st.divider()
                st.subheader("Cartera Detallada de Clientes Atendidos")
                if col_buyer in df_f.columns:
                    df_detalle_cli = df_f.groupby([col_buyer, col_pais]).agg(
                        VALOR_FOB_USD=('VALOR_FOB_USD', 'sum'),
                        NUM_TRANSACCIONES=('VALOR_FOB_USD', 'count')
                    ).reset_index().sort_values('VALOR_FOB_USD', ascending=False)
                    
                    df_detalle_cli['PORCENTAJE_PARTICIPACION'] = (df_detalle_cli['VALOR_FOB_USD'] / fob_total_prov * 100) if fob_total_prov > 0 else 0
                    df_detalle_cli.rename(columns={
                        col_buyer: 'COMPRADOR INTERNACIONAL', 
                        col_pais: 'PAÍS DESTINO', 
                        'VALOR_FOB_USD': 'VALOR TOTAL EXPORTADO (USD)', 
                        'NUM_TRANSACCIONES': 'CANTIDAD DE DESPACHOS', 
                        'PORCENTAJE_PARTICIPACION': '% PARTICIPACIÓN'
                    }, inplace=True)
                    
                    st.dataframe(df_detalle_cli.style.format({
                        'VALOR TOTAL EXPORTADO (USD)': '${:,.2f}', 
                        '% PARTICIPACIÓN': '{:.2f}%', 
                        'CANTIDAD DE DESPACHOS': '{:,}'
                    }).hide(axis='index'), use_container_width=True)
                
                with st.expander("Ver histórico completo de facturas/operaciones de exportación"):
                    cols_despacho = [c for c in ['FECHA', 'FECHA_PROCESO', 'SUBPARTIDA', 'DESCRIPCION', col_buyer, col_pais, 'VALOR_FOB_USD', 'KG_NETO'] if c in df_f.columns]
                    if cols_despacho:
                        st.dataframe(df_f[cols_despacho].style.format({'VALOR_FOB_USD': '${:,.2f}'}), use_container_width=True)
                    else:
                        st.dataframe(df_f.head(100), use_container_width=True)