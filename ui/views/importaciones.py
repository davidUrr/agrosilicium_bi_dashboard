# ui/views/importaciones.py
import streamlit as st
import pandas as pd
import plotly.express as px
from db_utils import read_from_db
from ui.components import (
    render_kpi_card, 
    render_grafico_pareto, 
    render_mapa_mundial
)
from ui.styles import HEX_VERDE_CORPORATIVO, HEX_VERDE_FRESCO

def mapear_pais_plotly(nombre_pais):
    """
    Convierte nombres de países en español (y variaciones DIAN/Confecámaras) 
    a su nombre estándar en inglés compatible con Plotly Choropleth (locationmode='country names').
    """
    if not nombre_pais or pd.isna(nombre_pais):
        return nombre_pais

    mapeo = {
        # --- A ---
        'AFGANISTAN': 'Afghanistan',
        'ALBANIA': 'Albania',
        'ALEMANIA': 'Germany',
        'ANDORRA': 'Andorra',
        'ANGUILA': 'Anguilla',
        'ARABIA SAUDITA': 'Saudi Arabia',
        'ARGENTINA': 'Argentina',
        'ARMENIA': 'Armenia',
        'ARUBA': 'Aruba',
        'AUSTRALIA': 'Australia',
        'AUSTRIA': 'Austria',

        # --- B ---
        'BELGICA': 'Belgium',
        'BELICE': 'Belize',
        'BERMUDAS': 'Bermuda',
        'BOLIVIA': 'Bolivia',
        'BRASIL': 'Brazil',
        'BRUNEI DARUSSALAM': 'Brunei',
        'BULGARIA': 'Bulgaria',

        # --- C ---
        'CAMBOYA': 'Cambodia',
        'CANADA': 'Canada',
        'CHEQUIA': 'Czech Republic',
        'CHILE': 'Chile',
        'CHINA': 'China',
        'CHIPRE': 'Cyprus',
        'COLOMBIA': 'Colombia',
        'ZONA FRANCA COLOMBIA': 'Colombia',
        'COREA (SUR) REPUBLICA DE': 'South Korea',
        'COREA DEL SUR': 'South Korea',
        'COSTA RICA': 'Costa Rica',
        'COTE D’IVOIRE': "Cote d'Ivoire",
        'CROACIA': 'Croatia',
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
        'GHANA': 'Ghana',
        'GRANADA': 'Grenada',
        'GRECIA': 'Greece',
        'GUATEMALA': 'Guatemala',
        'GUYANA': 'Guyana',

        # --- H ---
        'HAITI': 'Haiti',
        'HONDURAS': 'Honduras',
        'HONG KONG': 'Hong Kong',
        'HUNGRIA': 'Hungary',

        # --- I ---
        'INDIA': 'India',
        'INDONESIA': 'Indonesia',
        'IRAQ': 'Iraq',
        'IRLANDA': 'Ireland',
        'IRLANDA (EIRE)': 'Ireland',
        'ISLAS MARSHALL': 'Marshall Islands',
        'MARSHALL, ISLAS': 'Marshall Islands',
        'ISLAS VIRGENES BRITANICAS': 'British Virgin Islands',
        'VIRGENES ISLAS (BRITANICAS)': 'British Virgin Islands',
        'VIRGENES ISLAS (ESTADOS UNIDOS)': 'United States Virgin Islands',
        'ISRAEL': 'Israel',
        'ITALIA': 'Italy',

        # --- J ---
        'JAPON': 'Japan',

        # --- K ---
        'KAZAJSTAN': 'Kazakhstan',
        'KUWAIT': 'Kuwait',

        # --- L ---
        'LETONIA': 'Latvia',
        'LIBANO': 'Lebanon',
        'LIECHTENSTEIN': 'Liechtenstein',
        'LITUANIA': 'Lithuania',
        'LUXEMBURGO': 'Luxembourg',

        # --- M ---
        'MACAO': 'Macau',
        'MACEDONIA DEL NORTE': 'North Macedonia',
        'MALASIA': 'Malaysia',
        'MEXICO': 'Mexico',

        # --- N ---
        'NICARAGUA': 'Nicaragua',
        'NORUEGA': 'Norway',
        'NUEVA ZELANDA': 'New Zealand',

        # --- O ---
        'OMAN': 'Oman',

        # --- P ---
        'PAISES BAJOS': 'Netherlands',
        'PAKISTAN': 'Pakistan',
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
        'SAMOA': 'Samoa',
        'SAN MARINO': 'San Marino',
        'SENEGAL': 'Senegal',
        'SERBIA': 'Serbia',
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
        'TRINIDAD Y TABAGO': 'Trinidad and Tobago',
        'TRINIDAD Y TOBAGO': 'Trinidad and Tobago',
        'TUNEZ': 'Tunisia',
        'TURQUIA': 'Turkey',

        # --- U ---
        'UCRANIA': 'Ukraine',
        'URUGUAY': 'Uruguay',

        # --- V ---
        'VENEZUELA': 'Venezuela',
        'VIETNAM': 'Vietnam'
    }

    key = str(nombre_pais).strip().upper()
    return mapeo.get(key, nombre_pais)

def render_vista_importaciones():
    st.title("Inteligencia Competitiva de Importaciones")
    st.divider()

    # Carga de datasets
    datos_raw = read_from_db("impo_enriquecida")
    nichos_df = read_from_db("e02_top_importadores")
    pareto_df = read_from_db("e04_pareto_importacion")
    dispais_df = read_from_db("e05_dist_pais_impo")
    disprov_df = read_from_db("e05_dist_prov_impo")

    if datos_raw.empty:
        st.warning("No hay datos de importaciones en la base de datos central.")
        return

    # Normalización de columnas en memoria
    col_pais = 'PAIS_EXPORTADOR' if 'PAIS_EXPORTADOR' in datos_raw.columns else 'PAIS_ORIGEN'
    col_foreign = 'NOMBRE_EXPORTADOR_NORMALIZADO' if 'NOMBRE_EXPORTADOR_NORMALIZADO' in datos_raw.columns else 'NOMBRE_EXPORTADOR'

    # =========================================================================
    # FILTROS REACTIVOS EN LA BARRA LATERAL (3 NIVELES)
    # =========================================================================
    st.sidebar.subheader("Filtros de Importación")
    
    # 1. Filtro por Nicho
    opciones_nichos = sorted(list(datos_raw['NICHO'].dropna().unique()))
    nichos_sel = st.sidebar.multiselect("Filtrar por Nicho Comercial:", opciones_nichos, key="n_imp")
    
    # 2. Filtro por Subpartida
    df_sub = datos_raw[datos_raw['NICHO'].isin(nichos_sel)] if nichos_sel else datos_raw
    col_sub_raw = 'SUBPARTIDA_ARANCELARIA' if 'SUBPARTIDA_ARANCELARIA' in df_sub.columns else 'SUBPARTIDA'
    opciones_subs = sorted(list(df_sub[col_sub_raw].astype(str).dropna().unique()))
    subs_sel = st.sidebar.multiselect("Filtrar por Subpartida Arancelaria:", opciones_subs, key="s_imp")
    
    # 3. Filtro por País de Origen
    opciones_paises = sorted(list(datos_raw[col_pais].dropna().unique()))
    paises_sel = st.sidebar.multiselect("Filtrar por País de Origen:", opciones_paises, key="p_imp")

    # Función de filtrado dinámico
    def aplicar_filtros_imp(df, col_n='NICHO', col_s=col_sub_raw, col_p=col_pais):
        res = df.copy()
        if nichos_sel and col_n in res.columns:
            res = res[res[col_n].isin(nichos_sel)]
        if subs_sel and col_s in res.columns:
            res = res[res[col_s].astype(str).isin(subs_sel)]
        if paises_sel:
            if col_p in res.columns:
                res = res[res[col_p].isin(paises_sel)]
            elif 'PRINCIPAL_PAIS_ORIGEN' in res.columns:
                res = res[res['PRINCIPAL_PAIS_ORIGEN'].isin(paises_sel)]
            elif 'PAIS_ORIGEN' in res.columns:
                res = res[res['PAIS_ORIGEN'].isin(paises_sel)]
        return res

    # DataFrames filtrados dinámicamente
    df_datos_f = aplicar_filtros_imp(datos_raw)
    df_nichos_f = aplicar_filtros_imp(nichos_df, col_s='SUBPARTIDA')
    df_pareto_f = aplicar_filtros_imp(pareto_df, col_s='SUBPARTIDA_ARANCELARIA')
    df_dispais_f = aplicar_filtros_imp(dispais_df, col_s='SUBPARTIDA_ARANCELARIA', col_p='PAIS_ORIGEN')
    df_disprov_f = aplicar_filtros_imp(disprov_df, col_s='SUBPARTIDA_ARANCELARIA', col_p='PAIS_ORIGEN')

    if df_datos_f.empty:
        st.warning("No hay datos para los filtros seleccionados.")
        return

    # =========================================================================
    # 📊 TARJETAS KPI
    # =========================================================================
    k1, k2, k3, k4 = st.columns(4)
    total_fob = df_datos_f["VALOR_FOB_USD"].sum()
    render_kpi_card(k1, "TOTAL IMPORTADO (FOB)", f"USD ${total_fob:,.2f}")
    render_kpi_card(k2, "REGISTROS / DECLARACIONES", f"{len(df_datos_f):,} Docs")
    render_kpi_card(k3, "COMPRADORES / COMPETIDORES", f"{df_datos_f['NIT_IMPORTADOR'].nunique()} Empresas")
    render_kpi_card(k4, "PROVEEDORES INTERNACIONALES", f"{df_datos_f[col_foreign].nunique()} Fábricas")

    st.write("")

    # =========================================================================
    # 📑 PESTAÑAS COMPLETAS CON RECOMENDACIONES Y DESGLOSE EN TABLAS
    # =========================================================================
    tab_sust, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "1. Prospectos & Recomendaciones",
        "2. Estructura de Mercado (Pareto)", 
        "3. Competidores Importadores", 
        "4. Origen Geográfico", 
        "5. Proveedores Internacionales", 
        "6. Perfil del Importador", 
        "7. Perfil del Proveedor"
    ])

    # --- PESTAÑA ESTRATÉGICA: RECOMENDACIONES Y DESGLOSE EN TABLAS ---
    with tab_sust:
        st.subheader("Matriz de Oportunidades & Panel de Recomendaciones")
        st.caption("Estrategia comercial de sustitución de importaciones basada en los datos filtrados:")

        df_lead = df_datos_f.groupby(['NOMBRE_IMPORTADOR', 'NIT_IMPORTADOR']).agg(
            COMPRA_TOTAL_USD=('VALOR_FOB_USD', 'sum'),
            PAIS_PRINCIPAL_SUMINISTRO=(col_pais, lambda x: x.mode()[0] if len(x.mode())>0 else x.iloc[0]),
            NUM_IMPORTACIONES=('VALOR_FOB_USD', 'count')
        ).reset_index().sort_values('COMPRA_TOTAL_USD', ascending=False)

        # Excluir a Extrusiones S.A. de la prospección
        df_lead = df_lead[~df_lead['NOMBRE_IMPORTADOR'].astype(str).str.contains("EXTRUSIONES", na=False)]

        st.dataframe(
            df_lead.head(20).style.format({
                'COMPRA_TOTAL_USD': '${:,.2f}',
                'NUM_IMPORTACIONES': '{:,}'
            }).hide(axis='index'), 
            use_container_width=True
        )

        st.divider()
        st.subheader("Panel de Recomendaciones para Toma de Decisiones")
        st.caption("Análisis estratégico de sustitución de importaciones y diversificación comercial:")

        rec_col1, rec_col2, rec_col3, rec_col4 = st.columns(4)

        # 1. SUSTITUCIÓN COMERCIALMENTE VIABLE
        with rec_col1:
            st.markdown("##### 🟢 Sustitución Viable")
            compra_asia = df_datos_f[df_datos_f[col_pais].isin(['CHINA', 'VIETNAM', 'TAIWAN', 'INDIA'])]['VALOR_FOB_USD'].sum()
            st.success(f"Demanda asiática: **USD ${compra_asia:,.2f}**. Ofrecer producción nacional con entrega inmediata.")
            
            df_t_paises_imp = df_datos_f.groupby(col_pais).agg(
                TAMAÑO_USD=('VALOR_FOB_USD', 'sum')
            ).reset_index().sort_values('TAMAÑO_USD', ascending=False)
            df_t_paises_imp.rename(columns={col_pais: 'PAÍS ORIGEN'}, inplace=True)
            
            st.dataframe(
                df_t_paises_imp.head(15).style.format({'TAMAÑO_USD': '${:,.2f}'}).hide(axis='index'),
                use_container_width=True
            )

        # 2. HOMOLOGACIÓN DE MOLDES / PERFILES
        with rec_col2:
            st.markdown("##### 🔵 Homologación Moldes")
            top_sub = df_datos_f.groupby(col_sub_raw)['VALOR_FOB_USD'].sum().sort_values(ascending=False).index[0] if col_sub_raw in df_datos_f.columns else "N/A"
            st.info(f"Subpartida líder: **`{top_sub}`**. Priorizar desarrollo técnico de moldes en esta línea.")
            
            df_t_subs_imp = df_datos_f.groupby(col_sub_raw).agg(
                TAMAÑO_USD=('VALOR_FOB_USD', 'sum')
            ).reset_index().sort_values('TAMAÑO_USD', ascending=False)
            df_t_subs_imp.rename(columns={col_sub_raw: 'SUBPARTIDA'}, inplace=True)
            
            st.dataframe(
                df_t_subs_imp.head(15).style.format({'TAMAÑO_USD': '${:,.2f}'}).hide(axis='index'),
                use_container_width=True
            )

        # 3. OPORTUNIDAD EN CADENA DE SUMINISTRO (PROVEEDORES)
        with rec_col3:
            st.markdown("##### 🟡 Cadena Suministro")
            top_prov = df_datos_f.groupby(col_foreign)['VALOR_FOB_USD'].sum().sort_values(ascending=False).index[0] if col_foreign in df_datos_f.columns else "N/A"
            st.warning(f"Proveedor Top: **`{top_prov}`**. Evaluar alianzas de distribución o maquila directa.")
            
            df_t_prov_imp = df_datos_f.groupby(col_foreign).agg(
                TAMAÑO_USD=('VALOR_FOB_USD', 'sum')
            ).reset_index().sort_values('TAMAÑO_USD', ascending=False)
            df_t_prov_imp.rename(columns={col_foreign: 'PROVEEDOR EXTRANJERO'}, inplace=True)
            
            st.dataframe(
                df_t_prov_imp.head(15).style.format({'TAMAÑO_USD': '${:,.2f}'}).hide(axis='index'),
                use_container_width=True
            )

        # 4. CLIENTES LOCALES POTENCIALES (NUEVA COLUMNA)
        with rec_col4:
            st.markdown("##### 🟣 Clientes Prospectos")
            df_lead_filt = df_datos_f[~df_datos_f['NOMBRE_IMPORTADOR'].astype(str).str.contains("EXTRUSIONES", na=False)]
            top_imp = df_lead_filt.groupby('NOMBRE_IMPORTADOR')['VALOR_FOB_USD'].sum().sort_values(ascending=False).index[0] if not df_lead_filt.empty else "N/A"
            st.error(f"Comprador Top: **`{top_imp}`**. Prospecto clave para sustitución directa.")
            
            df_t_imp_lead = df_lead_filt.groupby('NOMBRE_IMPORTADOR').agg(
                TAMAÑO_USD=('VALOR_FOB_USD', 'sum')
            ).reset_index().sort_values('TAMAÑO_USD', ascending=False)
            df_t_imp_lead.rename(columns={'NOMBRE_IMPORTADOR': 'IMPORTADOR LOCAL'}, inplace=True)
            
            st.dataframe(
                df_t_imp_lead.head(15).style.format({'TAMAÑO_USD': '${:,.2f}'}).hide(axis='index'),
                use_container_width=True
            )

    # --- PESTAÑA 1: PARETO Y GRÁFICO DINÁMICO ---
    with tab1:
        st.subheader("Análisis de Pareto y Estructura de Importación")
        col_s_p = 'SUBPARTIDA_ARANCELARIA' if 'SUBPARTIDA_ARANCELARIA' in df_pareto_f.columns else 'SUBPARTIDA'
        
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

    # --- PESTAÑA 2: COMPETIDORES IMPORTADORES ---
    with tab2:
        if len(df_nichos_f) > 0:
            df_top = df_nichos_f.sort_values('VALOR_FOB_USD', ascending=False).head(10)
            st.plotly_chart(px.bar(df_top, x='VALOR_FOB_USD', y='NOMBRE_IMPORTADOR', orientation='h', color_discrete_sequence=[HEX_VERDE_FRESCO], template="plotly_white"), use_container_width=True)
            b_imp = st.text_input("Buscar competidor importador (Nombre o NIT):", key="b_imp_table")
            df_out = df_nichos_f.sort_values('RANKING_EN_NICHO')
            if b_imp:
                df_out = df_out[df_out['NOMBRE_IMPORTADOR'].astype(str).str.contains(b_imp.upper(), na=False) | df_out['NIT_IMPORTADOR'].astype(str).str.contains(b_imp, na=False)]
            st.dataframe(df_out.style.format({'VALOR_FOB_USD': '${:,.2f}', 'PORCENTAJE_DEL_MERCADO': '{:.2f}%'}).hide(), use_container_width=True)

    # --- PESTAÑA 3: ORIGEN GEOGRÁFICO Y MAPA MUNDIAL ---
    with tab3:
        if len(df_dispais_f) > 0:
            val_col = 'VALOR_USD' if 'VALOR_USD' in df_dispais_f.columns else 'VALOR_FOB_USD'
            g_p = df_dispais_f.groupby('PAIS_ORIGEN').agg({val_col:'sum'}).reset_index().sort_values(val_col, ascending=False)
            
            # Mapeo de nombres de países para compatibilidad con Plotly Choropleth
            g_p['PAIS_PLOTLY'] = g_p['PAIS_ORIGEN'].apply(mapear_pais_plotly)
            
            # Mapa Coroplético Mundial
            fig_mapa_imp = render_mapa_mundial(g_p, 'PAIS_PLOTLY', val_col, "Mapa Mundial de Origen de las Importaciones")
            st.plotly_chart(fig_mapa_imp, use_container_width=True)

            st.plotly_chart(px.bar(g_p.head(12), x='PAIS_ORIGEN', y=val_col, color_discrete_sequence=[HEX_VERDE_CORPORATIVO], template="plotly_white"), use_container_width=True)
            st.dataframe(df_dispais_f.style.format({val_col: '${:,.2f}'}).hide(), use_container_width=True)

    # --- PESTAÑA 4: PROVEEDORES INTERNACIONALES ---
    with tab4:
        col_prov = 'NOMBRE_PROVEEDOR_NORMALIZADO' if 'NOMBRE_PROVEEDOR_NORMALIZADO' in df_disprov_f.columns else 'NOMBRE_PROVEEDOR'
        if len(df_disprov_f) > 0:
            val_col = 'VALOR_USD' if 'VALOR_USD' in df_disprov_f.columns else 'VALOR_FOB_USD'
            g_pr = df_disprov_f.groupby(col_prov).agg({val_col:'sum'}).reset_index().sort_values(val_col, ascending=False)
            st.plotly_chart(px.bar(g_pr.head(15), x=val_col, y=col_prov, orientation='h', color_discrete_sequence=[HEX_VERDE_FRESCO], template="plotly_white"), use_container_width=True)
            b_prov = st.text_input("Filtrar por nombre del fabricante/proveedor extranjero:", key="b_prov_table")
            df_pr_r = df_disprov_f.copy()
            if b_prov: 
                df_pr_r = df_pr_r[df_pr_r[col_prov].astype(str).str.contains(b_prov.upper(), na=False)]
            st.dataframe(df_pr_r.style.format({val_col: '${:,.2f}'}).hide(), use_container_width=True)

    # --- PESTAÑA 5: PERFIL DEL IMPORTADOR ---
    with tab5:
        st.subheader("Auditoría de Compras y Suministro del Competidor Local")
        if 'NOMBRE_IMPORTADOR' in df_datos_f.columns:
            lista_i = sorted(list(df_datos_f['NOMBRE_IMPORTADOR'].dropna().unique()))
            i_foco = st.selectbox("Selecciona una Empresa en Colombia para auditar su portafolio de compras:", lista_i, key="f_i_imp")
            
            if i_foco:
                df_f = df_datos_f[df_datos_f['NOMBRE_IMPORTADOR'] == i_foco]
                fob_tot_imp = df_f['VALOR_FOB_USD'].sum()
                st.markdown(f"**Ficha de Inteligencia de Compras:** `{i_foco}`")
                
                sub_k1, sub_k2, sub_k3 = st.columns(3)
                render_kpi_card(sub_k1, "VALOR TOTAL COMPRADO (FOB)", f"USD ${fob_tot_imp:,.2f}")
                render_kpi_card(sub_k2, "DECLARACIONES RADICADAS", f"{len(df_f):,} Importaciones")
                render_kpi_card(sub_k3, "PROVEEDORES INTERNACIONALES", f"{df_f[col_foreign].nunique() if col_foreign in df_f.columns else 0} Fábricas")
                
                df_imp_origen = df_f.groupby(col_pais).agg(VALOR_FOB_USD=('VALOR_FOB_USD', 'sum')).reset_index().sort_values('VALOR_FOB_USD', ascending=False)
                st.plotly_chart(px.pie(df_imp_origen, values='VALOR_FOB_USD', names=col_pais, title="% Distribución Geográfica de Suministro", hole=0.4), use_container_width=True)
                
                st.divider()
                st.subheader("Matriz de Proveedores Internacionales y Fábricas de Origen")
                if col_foreign in df_f.columns:
                    df_detalle_prov = df_f.groupby([col_foreign, col_pais]).agg(
                        VALOR_FOB_USD=('VALOR_FOB_USD', 'sum'),
                        NUM_TRANSACCIONES=('VALOR_FOB_USD', 'count')
                    ).reset_index().sort_values('VALOR_FOB_USD', ascending=False)
                    
                    df_detalle_prov['PORCENTAJE_PARTICIPACION'] = (df_detalle_prov['VALOR_FOB_USD'] / fob_tot_imp * 100) if fob_tot_imp > 0 else 0
                    df_detalle_prov.rename(columns={
                        col_foreign: 'PROVEEDOR / FABRICANTE EXTRANJERO', 
                        col_pais: 'PAÍS ORIGEN', 
                        'VALOR_FOB_USD': 'VALOR TOTAL COMPRADO (USD)', 
                        'NUM_TRANSACCIONES': 'CANTIDAD DE DESPACHOS', 
                        'PORCENTAJE_PARTICIPACION': '% PARTICIPACIÓN'
                    }, inplace=True)
                    
                    st.dataframe(df_detalle_prov.style.format({
                        'VALOR TOTAL COMPRADO (USD)': '${:,.2f}', 
                        '% PARTICIPACIÓN': '{:.2f}%', 
                        'CANTIDAD DE DESPACHOS': '{:,}'
                    }).hide(axis='index'), use_container_width=True)
                
                with st.expander("Ver histórico completo de declaraciones / envíos recibidos"):
                    cols_despacho = [c for c in ['FECHA', 'FECHA_MANIFIESTO', 'SUBPARTIDA_ARANCELARIA', 'DESCRIPCION_MERCANCIA', col_foreign, col_pais, 'VALOR_FOB_USD', 'KG_NETO'] if c in df_f.columns]
                    if cols_despacho:
                        st.dataframe(df_f[cols_despacho].style.format({'VALOR_FOB_USD': '${:,.2f}'}), use_container_width=True)
                    else:
                        st.dataframe(df_f.head(100), use_container_width=True)

    # --- PESTAÑA 6: PERFIL DEL PROVEEDOR (EXTRANJERO) ---
    with tab6:
        st.subheader("Auditoría de Clientes del Fabricante Internacional")
        if col_foreign in df_datos_f.columns:
            lista_p = sorted(list(df_datos_f[col_foreign].dropna().unique()))
            p_foco = st.selectbox("Selecciona un Proveedor Internacional para auditar su red de distribución en Colombia:", lista_p, key="f_p_imp")
            
            if p_foco:
                df_f = df_datos_f[df_datos_f[col_foreign] == p_foco]
                fob_tot_prov = df_f['VALOR_FOB_USD'].sum()
                st.markdown(f"**Ficha de Inteligencia de Suministro:** `{p_foco}`")
                
                sub_pk1, sub_pk2, sub_pk3 = st.columns(3)
                render_kpi_card(sub_pk1, "VENTAS TOTALES A COLOMBIA", f"USD ${fob_tot_prov:,.2f}")
                render_kpi_card(sub_pk2, "DESPACHOS EMBARCADOS", f"{len(df_f):,} Envíos")
                render_kpi_card(sub_pk3, "CLIENTES CAPTURADOS EN PAÍS", f"{df_f['NOMBRE_IMPORTADOR'].nunique()} Importadores")
                
                df_prov_clientes = df_f.groupby('NOMBRE_IMPORTADOR').agg(VALOR_FOB_USD=('VALOR_FOB_USD', 'sum')).reset_index().sort_values('VALOR_FOB_USD', ascending=False)
                st.plotly_chart(px.bar(df_prov_clientes.head(10), x='VALOR_FOB_USD', y='NOMBRE_IMPORTADOR', orientation='h', title="Top Clientes en Colombia", color_discrete_sequence=[HEX_VERDE_CORPORATIVO]), use_container_width=True)
                
                st.divider()
                st.subheader("Detalle de Entregas a Importadores Colombianos")
                df_detalle_imp = df_f.groupby('NOMBRE_IMPORTADOR').agg(
                    VALOR_FOB_USD=('VALOR_FOB_USD', 'sum'),
                    NUM_TRANSACCIONES=('VALOR_FOB_USD', 'count')
                ).reset_index().sort_values('VALOR_FOB_USD', ascending=False)
                
                df_detalle_imp['PORCENTAJE_PARTICIPACION'] = (df_detalle_imp['VALOR_FOB_USD'] / fob_tot_prov * 100) if fob_tot_prov > 0 else 0
                df_detalle_imp.rename(columns={
                    'NOMBRE_IMPORTADOR': 'IMPORTADOR / CLIENTE COLOMBIANO', 
                    'VALOR_FOB_USD': 'VALOR TOTAL COMPRADO (USD)', 
                    'NUM_TRANSACCIONES': 'CANTIDAD DE DESPACHOS', 
                    'PORCENTAJE_PARTICIPACION': '% PARTICIPACIÓN'
                }, inplace=True)
                
                st.dataframe(df_detalle_imp.style.format({
                    'VALOR TOTAL COMPRADO (USD)': '${:,.2f}', 
                    '% PARTICIPACIÓN': '{:.2f}%', 
                    'CANTIDAD DE DESPACHOS': '{:,}'
                }).hide(axis='index'), use_container_width=True)
                
                with st.expander("Ver histórico completo de importaciones registradas"):
                    cols_despacho = [c for c in ['FECHA', 'FECHA_MANIFIESTO', 'SUBPARTIDA_ARANCELARIA', 'DESCRIPCION_MERCANCIA', 'NOMBRE_IMPORTADOR', col_pais, 'VALOR_FOB_USD', 'KG_NETO'] if c in df_f.columns]
                    if cols_despacho:
                        st.dataframe(df_f[cols_despacho].style.format({'VALOR_FOB_USD': '${:,.2f}'}), use_container_width=True)
                    else:
                        st.dataframe(df_f.head(100), use_container_width=True)