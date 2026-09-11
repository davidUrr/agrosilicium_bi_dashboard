# ui/__init__.py
"""
Módulo de Interfaz de Usuario (UI) para la Suite de Inteligencia de Mercado de Extrusiones S.A.
"""

from ui.styles import aplicar_estilos_corporativos, HEX_VERDE_CORPORATIVO, HEX_VERDE_FRESCO
from ui.components import (
    render_kpi_card, 
    render_grafico_pareto, 
    render_grafico_barras_horizontal,
    render_mapa_mundial,
    render_matriz_priorizacion_nichos
)

__all__ = [
    "aplicar_estilos_corporativos",
    "HEX_VERDE_CORPORATIVO",
    "HEX_AZUL_ACERO",
    "render_kpi_card",
    "render_grafico_pareto",
    "render_grafico_barras_horizontal",
    "render_mapa_mundial",
    "render_matriz_priorizacion_nichos"
]