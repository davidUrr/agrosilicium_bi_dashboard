# ui/components.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from ui.styles import HEX_VERDE_CORPORATIVO, HEX_VERDE_FRESCO

def render_kpi_card(col, titulo: str, valor: str):
    """Renderiza una tarjeta KPI uniforme estilizada."""
    col.markdown(
        f'<div class="metric-box"><h6>{titulo.upper()}</h6><h2>{valor}</h2></div>', 
        unsafe_allow_html=True
    )

def render_grafico_pareto(df, col_etiqueta, col_valor, col_acumulado):
    """Genera un gráfico mixto Plotly (Barras de monto + Línea de % acumulado)."""
    fig = go.Figure([
        go.Bar(
            x=df[col_etiqueta], 
            y=df[col_valor], 
            marker_color=HEX_VERDE_CORPORATIVO, 
            name="USD"
        ), 
        go.Scatter(
            x=df[col_etiqueta], 
            y=df[col_acumulado], 
            yaxis="y2", 
            name="% Acum", 
            line=dict(color="#D9534F", width=3)
        )
    ])
    fig.update_layout(
        yaxis2=dict(overlaying="y", side="right", range=[0, 105]), 
        template="plotly_white", 
        xaxis=dict(tickangle=35)
    )
    return fig

def render_grafico_barras_horizontal(df, col_x, col_y, titulo=""):
    """Genera un gráfico horizontal estandarizado en Azul Acero."""
    return px.bar(
        df, x=col_x, y=col_y, orientation='h', title=titulo,
        color_discrete_sequence=[HEX_VERDE_FRESCO], template="plotly_white"
    )

def render_mapa_mundial(df, col_pais, col_valor, titulo=""):
    """Genera un mapa coroplético mundial interactivo."""
    fig = px.choropleth(
        df,
        locations=col_pais,
        locationmode='country names',
        color=col_valor,
        hover_name=col_pais,
        color_continuous_scale='Blues',
        title=titulo,
        template='plotly_white'
    )
    fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
    return fig

def render_matriz_priorizacion_nichos(df, col_nicho, col_valor, col_competidores):
    """Genera una matriz de burbujas para evaluar atracción vs. competencia en nichos."""
    fig = px.scatter(
        df,
        x=col_competidores,
        y=col_valor,
        size=col_valor,
        color=col_nicho,
        hover_name=col_nicho,
        text=col_nicho,
        labels={
            col_competidores: "N° de Competidores / Actores en el Mercado",
            col_valor: "Tamaño del Mercado (USD FOB)"
        },
        title="Matriz Estratégica: Tamaño de Mercado vs. Concentración de Competencia",
        template="plotly_white"
    )
    fig.update_traces(textposition='top center')
    return fig