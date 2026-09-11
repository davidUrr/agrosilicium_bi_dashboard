# ui/views/__init__.py
"""
Submódulos de vista para cada uno de los enfoques de mercado del dashboard.
"""

from ui.views.exportaciones import render_vista_exportaciones
from ui.views.importaciones import render_vista_importaciones
from ui.views.financiera import render_vista_financiera

__all__ = [
    "render_vista_exportaciones",
    "render_vista_importaciones",
    "render_vista_financiera"
]